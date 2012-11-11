using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace Client
{
    class Program
    {
        public static bool exit;
        public static void Main(string[] args)
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
            Console.WriteLine("\nType help for a list of commands.");
            ConsoleKeyListener.Start();
            while ((!exit))
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
            string ConsoleInput;
            Program threadlistener = new Program();
            while (true)
            {
                ConsoleInput = Console.ReadLine();
                switch (ConsoleInput.ToLower())
                {
                    case "quit":
                        Console.WriteLine("You reached the exit-block");
                        threadlistener.Client.Disconnect(false);
                        Console.WriteLine("You should be disconnected now");
                        Environment.Exit(0);
                        break;
                    case "exit":
                        goto case "quit";
                    case "help":
                        Console.WriteLine("The available commands are:\nhelp: Opens this list.\nexit: see quit.\nquit: Closes the consolewindow, killing the client.");
                        break;
                    //case (StartsWith("send")):

                    default:
                        Console.WriteLine("Unknown command. Try the 'help' command for a list of commands'");
                        break;
                }
            }
        }
    }
}
