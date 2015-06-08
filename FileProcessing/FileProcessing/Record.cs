using System.Security.Cryptography;
using System.Text;

namespace FileProcessing{


    namespace ExtendsHash
    {
        /// <summary>
        /// 데이터를 저장하기 위한 레코드
        /// </summary>
        struct Record
        {
            private static MD5CryptoServiceProvider md5builder = new MD5CryptoServiceProvider();
            public string name;
            public string phone;
            public string address;
            public string major;

            /// <summary>
            /// 각 레코드의 키는 이름의 해시 값
            /// </summary>
            /// <returns>키를 md5로 해싱한 값을 하나로 합친 값</returns>
            override public int GetHashCode()
            {
                var byteArr = Encoding.Unicode.GetBytes(name);
                var resultArr = md5builder.ComputeHash(byteArr);
                var hash = 0;
                for (var i = 0; i < resultArr.Length; i++)
                {
                    hash += resultArr[i];
                }

                return hash;
            }

            override public string ToString()
            {
                StringBuilder sb = new StringBuilder();
                sb.Append(name);
                sb.Append(", ");
                sb.Append(phone);
                sb.Append(", ");
                sb.Append(address);
                sb.Append(", ");
                sb.Append(major);
                return sb.ToString();
            }

            override public bool Equals(object obj)
            {
                Record r = (Record)obj;
                return name.Equals(r.name) && address.Equals(r.address) && phone.Equals(r.phone) && major.Equals(r.major);
            }

            public static bool operator ==(Record r1, Record r2)
            {
                return r1.Equals(r2);
            }

            public static bool operator !=(Record r1, Record r2)
            {
                return !r1.Equals(r2);
            }
        }
    }
}