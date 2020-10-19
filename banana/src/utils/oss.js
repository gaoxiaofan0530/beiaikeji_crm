let OSS = require('ali-oss');

let client = new OSS({
  accessKeyId: 'LTAI4G4eX8xFa1eoZrLDdxKo',   // 你创建的Bucket时获取的
  accessKeySecret: 'jSHhRQsJnt4i9C2Bfd7kc1pIQkdQLN',  // 你创建的Bucket时获取的
  secure:true,
  bucket: 'beiaikeji-ow-img',  // 你创建的Bucket名称
  region: 'oss-cn-hangzhou'   //  你所购买oss服务的区域，默认oss-cn-hangzhou
});
    
export async function put (filePath, file) {
    try {
      let result = await client.put(filePath, file)
      return result
    } catch (err) {
      console.log(err)
    }
  }