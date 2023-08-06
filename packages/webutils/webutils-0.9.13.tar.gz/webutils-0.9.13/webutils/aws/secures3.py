import hmac
import time
import boto3
import base64
import hashlib
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class SecureS3(object):
    def __init__(self, key, secret_key):
        self.key = key
        self.secret_key = secret_key

    def gen_signature(self, string_to_sign):
        return base64.encodestring(
            hmac.new(
                self.secret_key.encode('utf-8'),
                string_to_sign,
                hashlib.sha1,
            ).digest()
        ).strip()

    def get_file_details(self, url):
        ''' Returns bucket name and file from an S3 URL
        '''
        amazon_host = 's3.amazonaws.com'
        s = urlparse(url)
        if not s.path or not s.path[1:]:
            raise ValueError('Invalid S3 file passed.')

        if s.netloc == amazon_host:
            # s3.amazonaws.com/bucket/file...
            bucket = s.path[1:].split('/')[0]
            filename = '/'.join(s.path[1:].split('/')[1:])
        elif s.netloc.endswith('.%s' % amazon_host):
            # bucket_name.s3.amazonaws.com/file...
            bucket = s.netloc.replace('.%s' % amazon_host, '')
            filename = s.path[1:]
        else:
            # bucket.com/file... (CNAME BUCKET URL)
            bucket = s.netloc
            filename = s.path[1:]

        return (bucket, filename, s.scheme)

    def get_auth_link(self, bucket, filename, scheme='https', expires=300,
                      timestamp=None, client_method='get_object'):
        ''' Return a secure S3 link with an expiration on the download.

            key: S3 Access Key (login)
            secret_key: S3 Secret Access Key (password)
            bucket: Bucket name
            filename: file path
            expires: Seconds from NOW the link expires
            timestamp: Epoch timestamp. If present, "expires" will not be used.
            client_method: The client method to generate the presigned url
        '''
        filename = quote_plus(filename)
        filename = filename.replace('%2F', '/')

        if timestamp is not None:
            expires_in = int(timestamp - time.time())
        else:
            expires_in = expires

        s3_client = boto3.client(
            's3',
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret_key,
        )
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params={'Bucket': bucket, 'Key': filename},
            ExpiresIn=expires_in,
        )
        return url

    def get_easy_auth_link(
        self,
        url,
        expires=600,
        client_method='get_object',
        use_bucket=None,
    ):
        ''' url should be the full URL to the secure file hosted on S3.
            examples:
            http://s3.amazonaws.com/your-bucket/yourfile.zip
            http://your-bucket.s3.amazonaws.com/yourfile.zip
            http://media.your-domain.com/yourfile.zip  (CNAME path to S3)
        '''
        try:
            bucket, fname, scheme = self.get_file_details(url)
        except ValueError:
            return None

        if use_bucket is not None:
            bucket = use_bucket

        return self.get_auth_link(
            bucket,
            fname,
            scheme=scheme,
            expires=expires,
            client_method=client_method,
        )
