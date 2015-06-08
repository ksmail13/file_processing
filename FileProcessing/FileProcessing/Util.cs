using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FileProcessing
{
    class Util
    {
        static public void log(string msg, params object[] objs)
        {
            StackTrace st = new StackTrace();
            StackFrame sf = st.GetFrame(1);
            sf.GetFileColumnNumber();
            Console.Write("[{0}] ", sf.GetMethod().Name);
            Console.WriteLine(msg, objs);
        }

        static public int GeneratePadding(int depth)
        {
            return (1 << depth) - 1;
        }

        static public bool IsSameHash(int depth, object o1, object o2)
        {
            int o1hash = PaddedHash(depth, o1);
            int o2hash = PaddedHash(depth, o2);
            return o1hash == o2hash;
        }

        static public int PaddedHash(int depth, object o)
        {
            int padding = GeneratePadding(depth);
            return o.GetHashCode() & padding;
        }

        public static int BitOn(int pos, int n)
        {
            n |= (1 << (pos - 1));

            return n;
        }
    }
}
