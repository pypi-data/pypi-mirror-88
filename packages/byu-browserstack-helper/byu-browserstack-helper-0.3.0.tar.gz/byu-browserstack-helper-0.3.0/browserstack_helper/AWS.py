import string
import boto3
import sys


def retrieve_ssm(parameter_name: string) -> string:
    try:
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        tester_password = (parameter['Parameter']['Value'])
        return tester_password
    except:
        print('Could not connect to AWS. Please log in to AWS and try again.')
        return None
