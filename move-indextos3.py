import boto3
import datetime

s3 = boto3.client('s3')
print('Attempting to upload index.html to saftb.raaps.net bucket...')
file = open('frontend\\code\\index.html', 'rb')
response = s3.put_object(
    Body=file,
    Bucket='saftb.raaps.net',
    Key='index.html',
    ContentType='text/html'
)
print(response)

file.close()

# cloudfront = boto3.client('cloudfront')
# print('Invalidating Cloudfront cache of old index.html')
# response = cloudfront.create_invalidation(
#     DistributionId='E2JYLM4FTU1VJY',
#     InvalidationBatch={
#         'Paths': {
#             'Quantity': 1,
#             'Items': [
#                 '/index.html'
#             ]
#         },
#         'CallerReference': datetime.datetime.now().isoformat()
#     }
# )
# print(response)