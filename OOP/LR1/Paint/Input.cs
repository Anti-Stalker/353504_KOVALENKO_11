internal class Input
{
    public int CorrectInput()
    {
        int output = 0;

        int count = 1;

        while (true)
        {
            Console.Write("Input number: ");
            string input = Console.ReadLine();

            if (int.TryParse(input, out int number))
            {
                output = number;
                for (int i = 0; i < count-1; i++)
                {
                    Console.SetCursorPosition(0, Console.CursorTop - 1);
                    Console.Write(new string(' ', Console.WindowWidth));
                    Console.SetCursorPosition(0, Console.CursorTop);
                }
                break;
            }
            else
            {
                for (int i = 0; i < count; i++)
                {
                    Console.SetCursorPosition(0, Console.CursorTop - 1);
                    Console.Write(new string(' ', Console.WindowWidth));
                    Console.SetCursorPosition(0, Console.CursorTop);
                }

                Console.WriteLine("Error! Input correct number.");

                count = 2;
            }
        }

        Console.SetCursorPosition(0, Console.CursorTop - 1);
        Console.Write(new string(' ', Console.WindowWidth));
        Console.SetCursorPosition(0, Console.CursorTop);

        return output;
    }
}

