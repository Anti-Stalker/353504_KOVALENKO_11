

using System;

internal class Menu
{
    public void Selector()
    {

        int startRow = 9;
        int endRow = 57;

        int frameWidth = 210;

        for (int row = startRow; row <= endRow; row++)
        {
   
            Console.SetCursorPosition(0, row);

            if (row == startRow || row == endRow)
            {

                Console.WriteLine(new string('$', frameWidth));
            }
            else
            {

                Console.Write('$');
                Console.SetCursorPosition(frameWidth - 1, row);
                Console.Write('$');
            }
        }

        Console.SetCursorPosition(0, endRow + 1);


        Console.SetCursorPosition(0, 0);

        Console.WriteLine("0 - draw; 1 - erase; 2 - move; 3 - add background; 4 - save canfas; 5 - load from canvas; 6 - undo; 7 - redo; 8 - exit");

        Action action = new Action();

        Input input = new Input();


        while (true)
        {
            int a = input.CorrectInput();

            int ptr = Console.CursorTop;

            action.Execute(a);


            Console.SetCursorPosition(0, ptr);

            Console.Write(new string(' ', Console.WindowWidth));
            Console.SetCursorPosition(0, Console.CursorTop);
        }
    }
}