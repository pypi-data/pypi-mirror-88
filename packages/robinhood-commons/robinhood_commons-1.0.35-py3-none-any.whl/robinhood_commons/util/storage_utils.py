import pickle
from typing import Any

from robinhood_commons.util.aws_utils import AwsUtils

SERVICE_NAME: str = 's3'
BUCKET_NAME: str = 'robinhood-day-trader'
UTF: str = 'utf-8'


class StorageUtils:

    @classmethod
    def client(cls):
        return AwsUtils.get_resource(name=SERVICE_NAME)

    @classmethod
    def get_bucket(cls):
        return cls.client().Bucket(BUCKET_NAME)

    @classmethod
    def get(cls, path: str):
        print(f'getting to {StorageUtils.get_bucket()}...path: {path}')
        return pickle.loads(cls.client().Object(BUCKET_NAME, path).get()['Body'].read())

    @classmethod
    def upload(cls, path: str, data: Any) -> None:
        print(f'putting to {StorageUtils.get_bucket()}...path: {path}')
        StorageUtils.get_bucket().put_object(Key=path, Body=pickle.dumps(data))


def main():
    StorageUtils.upload(path='stocks.json',
                        data=["AAPL", "FRAF", "IPI", "NLOK", "WHR", "FB", "BIIB", "PINS", "DRRX", "IDN"])

    print(StorageUtils.get(path='stocks.json'))


if __name__ == '__main__':
    main()
