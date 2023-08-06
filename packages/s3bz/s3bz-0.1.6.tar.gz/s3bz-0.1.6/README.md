# S3Bz
> save and load dictionary to s3 using bz compression


## Install

`pip install s3bz`

## How to use

### Create a bucket and make sure that it has transfer acceleration enabled
#### create a buket
`aws s3 mb s3://<bucketname>`
#### put transfer acceleration
`aws s3api put-bucket-accelerate-configuration --bucket <bucketname> --accelerate-configuration Status=Enabled`

First, import the s3 module

## import package

```python
from importlib import reload
from s3bz.s3bz import S3
```

### set up dummy data

## BZ2 compression

### save object using bz2 compression

```python
result = S3.save(key = key, 
       objectToSave = sampleDict,
       bucket = bucket,
       user=USER,
       pw = PW,
       accelerate = True)
print(('failed', 'success')[result])
```

    success


### load object with bz2 compression

```python
result = S3.load(key = key,
       bucket = bucket,
       user = USER,
       pw = PW,
       accelerate = True)
print(result[0])
```

    {'ib_prcode': '75233', 'ib_brcode': '1004', 'ib_cf_qty': '155', 'new_ib_vs_stock_cv': '880'}


## other compressions
Zl : zlib compression with json string encoding
pklzl : zlib compression with pickle encoding

```python
print(bucket)
%time S3.saveZl(key,sampleDict,bucket)
%time S3.loadZl(key,bucket)
%time S3.savePklZl(key,sampleDict,bucket)
%time result =S3.loadPklZl(key,bucket)
```

    pybz-test
    CPU times: user 22.1 ms, sys: 728 µs, total: 22.9 ms
    Wall time: 134 ms
    CPU times: user 42.6 ms, sys: 0 ns, total: 42.6 ms
    Wall time: 542 ms
    CPU times: user 19.3 ms, sys: 0 ns, total: 19.3 ms
    Wall time: 150 ms
    CPU times: user 41 ms, sys: 3.28 ms, total: 44.3 ms
    Wall time: 503 ms


## Bring your own compressor and encoder

```python
import gzip, json
compressor=lambda x: gzip.compress(x)
encoder=lambda x: json.dumps(x).encode()
decompressor=lambda x: gzip.decompress(x)
decoder=lambda x: json.loads(x.decode())

%time S3.generalSave(key, sampleDict, bucket = bucket, compressor=compressor, encoder=encoder )
%time result = S3.generalLoad(key, bucket , decompressor=decompressor, decoder=decoder)
assert result == sampleDict, 'not the same as sample dict'
```

    CPU times: user 30.4 ms, sys: 0 ns, total: 30.4 ms
    Wall time: 128 ms
    CPU times: user 44.8 ms, sys: 0 ns, total: 44.8 ms
    Wall time: 416 ms


## check if an object exist

```python
result = S3.exist('', bucket, user=USER, pw=PW, accelerate = True)
print(('doesnt exist', 'exist')[result])
```

    exist


## presign download object

```python
url = S3.presign(key=key,
              bucket=bucket,
              expiry = 1000,
              user=USER,
              pw=PW)
print(url)
```

### download using signed link

```python
from s3bz.s3bz import Requests
result = Requests.getContentFromUrl(url)
```

## File operations

### save without compression

```python
inputPath = '/tmp/tmpFile.txt'
key = 'tmpFile'
downloadPath = '/tmp/downloadTmpFile.txt'
with open(inputPath , 'w')as f:
  f.write('hello world')
```

```python
S3.saveFile(key =key ,path = inputPath,bucket = bucket)
##test
S3.exist(key,bucket)
```

### load without compression

```python
S3.loadFile(key= key , path = downloadPath, bucket = bucket)
```

```python
##test
with open(downloadPath, 'r') as f:
  print(f.read())
```

### delete

```python
result = S3.deleteFile(key, bucket)
## test
S3.exist(key,bucket)
```

## save and load pandas dataframe

```python
### please install in pandas, 
### this is not include in the requirements to minimize the size impact
import pandas as pd
df = pd.DataFrame({'test':[1,2,3,4,5],'test2':[2,3,4,5,6]})
S3.saveDataFrame(bucket,key,df)
S3.loadDataFrame(bucket,key)
```
