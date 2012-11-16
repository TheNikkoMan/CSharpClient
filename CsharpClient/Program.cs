using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

// TODO:
// Shut down cleanly. Access the NetworkStream stream from the keylistener thread, and .Shutdown and .Disconnect
// Send messages back to the server

namespace Client
{
    public class Program
    {
        public static bool exit;
        public static NetworkStream stream;
        public static StreamWriter sw;

        public static void sendToServer(string fuckedMessage)
        {
            Console.WriteLine("fuckedMessage is: " + fuckedMessage);
            string[] Almostmessage = fuckedMessage.Split( ' ' );
            string message = Almostmessage[1];
            Console.WriteLine("message is: " + message);
            sw.WriteLine(message);
            sw.Flush();
        }

        public static void ListerKeyBoardEvent()
        {
            string ConsoleInput;
            while (true)
            {
                ConsoleInput = Console.ReadLine();
                string lowerconsoleinput = Console.ReadLine().ToLower();
                if ((lowerconsoleinput == "quit") || (lowerconsoleinput == "exit"))
                {
                    exit = true;
                }
                else if (lowerconsoleinput.StartsWith("send "))
                {
                    sendToServer(ConsoleInput);
                }
                else if (lowerconsoleinput == "help")
                {
                    Console.WriteLine("The available commands are:\nhelp: Opens this list.\nexit: see quit.\nquit: Closes the consolewindow, killing the client.");
                }
                else
                {
                    Console.WriteLine("Unknown command. Try the 'help' command for a list of commands");
                }
            }
        }

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
            else if (!(Int32.TryParse(PortString, out localPort)))
            {
                Console.WriteLine("The port you specified was invalid. Please enter it again.");
                goto connectPort;
            }
            else
            {
                localPort = Int32.Parse(PortString);
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
            StreamWriter streamwriter = new StreamWriter(stream);
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
            Console.WriteLine("Success! You should be able to exit now!"); // Environment.Exit(0);
        }
    }
}
