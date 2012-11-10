using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;


// TODO:
// 1. Catch System.Net.Sockets.SocketException and retry connection DONE DONE
// 2. Enable q to quit DONE DONE






namespace Client
{
    class Program
    {
        static void Main(string[] args)
        {
            int localPort = 27000;
            int bufferSize = 200;
            string host;
            string PortString;
            TcpClient listener;
            Console.WriteLine("Please input the host address and the port number you want to connect to, separated by a press on Return. \nEnter nothing for localhost:27000");
            connectHost:
            Console.Write("Host: ");
            host = Console.ReadLine();
            try
            {
                Dns.GetHostEntry(host);
            }
            catch (SocketException)
            {
                Console.WriteLine("The IP address you entered was invalid. Please try again.");
                goto connectHost;
            }
            if (String.IsNullOrEmpty(host))
            {
                host = "localhost";
            }
        connectPort:
            Console.Write("Port: ");
            PortString = Console.ReadLine();
            if (String.IsNullOrEmpty(PortString))
            {
                PortString = "27000";
                localPort = 27000;
            }
            else
            {

                if (!(Int32.TryParse(PortString, out localPort)))
                {
                    Console.WriteLine("The port you specified was invalid. Please enter it again.");
                    goto connectPort;
                }
            }
            byte[] ByteBuffer = new byte[bufferSize];
            try
            {
                listener = new TcpClient(host, localPort);
            }
            catch (SocketException)
            {
                Console.WriteLine("A socket error occured. Please recheck that the \nserver hostname or IP address is correct, and that the server is running.\n");
                goto connectHost;
            }
            NetworkStream stream = listener.GetStream();
            Thread ConsoleKeyListener = new Thread(new ThreadStart(ListerKeyBoardEvent));
            //StreamWriter writeStream = new StreamWriter(stream);
            Console.WriteLine("Press the Q key at any time to exit");
            ConsoleKeyListener.Start();
            while (true)
            {
                stream.Read(ByteBuffer, 0, bufferSize);
                string returndata = Encoding.UTF8.GetString(ByteBuffer.Reverse().SkipWhile(x => x == 0).Reverse().ToArray());
                Console.WriteLine("The string recieved is: " + returndata.Replace("z_*", " "));
                Console.WriteLine("The bytes recieved are: " + BitConverter.ToString(ByteBuffer.Reverse().SkipWhile(x => x == 0).Reverse().ToArray()));
                Array.Clear(ByteBuffer, 0, bufferSize);
            }
        }

        public static void ListerKeyBoardEvent()
        {
            do
            {
                if (Console.ReadKey(true).Key == ConsoleKey.Q)
                {
                    Environment.Exit(0);
                }
            } while (true);
        }
    }
}
