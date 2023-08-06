'''
    Requires Boto3 AWS SDK for Python
    https://github.com/boto/boto3
'''
import boto3
import logging
import botocore
import mimetypes

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

log = logging.getLogger('webutils.aws.s3proc')


class S3Error(Exception):
    'Misc. S3 Service Error'
    pass


def checkbucket(view_func):
    def _checkbucket(self, *args, **kwargs):
        if self.bucket is None:
            raise S3Error('No assigned bucket. Must run connect()')
        return view_func(self, *args, **kwargs)
    return _checkbucket


class S3Proc(object):
    def __init__(self, aws_key, aws_secret_key,
                 bucket, bucket_validate=False, default_perm='private'):
        self.aws_key = aws_key
        self.aws_secret_key = aws_secret_key
        self.bucket_name = bucket
        self.bucket_validate = bucket_validate
        self.conn = None
        self.bucket = None
        self.perm_tuple = (
            'private',
            'public-read',
            'public-read-write',
            'authenticated-read',
        )
        if default_perm not in self.perm_tuple:
            default_perm = 'private'
        self.default_perm = default_perm

    def _get_perm(self, perm=None):
        if perm is None or (perm is not None and perm not in self.perm_tuple):
            perm = self.default_perm
        return perm

    def connect(self):
        boto3.setup_default_session(
            aws_access_key_id=self.aws_key,
            aws_secret_access_key=self.aws_secret_key,
        )
        self.conn = boto3.resource('s3')
        self.bucket = self.conn.Bucket(self.bucket_name)
        self.client = self.conn.meta.client
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                self.conn.create_bucket(Bucket=self.bucket_name)
        return True

    @checkbucket
    def put(self, filename, data, perm=None, fail_silently=True):
        perm = self._get_perm(perm)
        kwargs = {'Body': data, 'ACL': perm}
        try:
            ctype = mimetypes.guess_type(filename)[0]
            if ctype:
                kwargs['ContentType'] = ctype
        except IndexError:
            pass
        self.bucket.Object(filename).put(**kwargs)
        return True

    @checkbucket
    def put_from_file(self, filename, remote_filename=None,
                      perm=None, fail_silently=True):
        ''' Upload file from disk. If you want a different
            remote filename, specify in remote_filename
        '''
        try:
            fp = open(filename, 'rb')
            r_path = remote_filename if remote_filename else filename
            self.put(r_path, fp, perm)
            fp.close()
            return True
        except Exception as e:
            log.error('Failed file upload: {0}'.format(str(e)))
            pass
        return False

    @checkbucket
    def get_file_key(self, filename):
        ''' Returns a Key object. Use key['Body'].read()
        '''
        try:
            return self.bucket.Object(filename).get()
        except botocore.exceptions.ClientError as error:
            raise S3Error('Error: {0}: {1}'.format(
                error.response['ResponseMetadata']['HTTPStatusCode'],
                error.response['Error']['Message']))

    @checkbucket
    def get(self, filename):
        ''' Returns file data
        '''
        key = self.get_file_key(filename)
        _file = StringIO(key['Body'].read())
        return _file

    @checkbucket
    def get_to_file(self, filename, local_filename=None):
        ''' Save file to local filename.
        '''
        try:
            self.bucket.Object(filename).download_file(
                local_filename if local_filename else filename)
        except botocore.exceptions.ClientError as error:
            raise S3Error('Error: {0}: {1}'.format(
                error.response['ResponseMetadata']['HTTPStatusCode'],
                error.response['Error']['Message']))
        return True

    @checkbucket
    def delete(self, filename, fail_silently=True):
        ''' Returns true/false on delete
            Raises S3Error if fail_silently is set to False
        '''
        self.bucket.Object(filename).delete()
        return True

    @checkbucket
    def get_perm(self, filename):
        ''' Returns permissions for set file.
        '''
        try:
            return self.conn.ObjectAcl(self.bucket_name, filename)
        except botocore.exceptions.ClientError as error:
            raise S3Error('Error: {0}: {1}'.format(
                error.response['ResponseMetadata']['HTTPStatusCode'],
                error.response['Error']['Message']))

    @checkbucket
    def set_perm(self, filename, perm, fail_silently=True):
        ''' Sets permissions on file.
        '''
        perm = self._get_perm(perm)
        try:
            object_acl = self.conn.ObjectAcl(self.bucket_name, filename)
            object_acl.put(ACL=perm)
        except botocore.exceptions.ClientError as error:
            raise S3Error('Error: {0}: {1}'.format(
                error.response['ResponseMetadata']['HTTPStatusCode'],
                error.response['Error']['Message']))
        return True

    @checkbucket
    def set_metadata(self, filename, meta_key, meta_value):
        try:
            k = self.client.head_object(Bucket=self.bucket_name, Key=filename)
            m = k['Metadata']
            m[meta_key] = meta_value
            copy_source = '{0}/{1}'.format(self.bucket_name, filename)
            self.client.copy_object(
                Bucket=self.bucket_name,
                Key=filename,
                CopySource=copy_source,
                Metadata=m,
                MetadataDirective='REPLACE',
            )
        except botocore.exceptions.ClientError as error:
            raise S3Error('Error: {0}: {1}'.format(
                error.response['ResponseMetadata']['HTTPStatusCode'],
                error.response['Error']['Message']))
        return True

    @checkbucket
    def get_metadata(self, filename, meta_key):
        try:
            k = self.client.head_object(Bucket=self.bucket_name, Key=filename)
        except botocore.exceptions.ClientError as error:
            raise S3Error('Error: {0}: {1}'.format(
                error.response['ResponseMetadata']['HTTPStatusCode'],
                error.response['Error']['Message']))
        try:
            m = k['Metadata']
            return m[meta_key]
        except KeyError:
            raise S3Error('Invalid meta key')
