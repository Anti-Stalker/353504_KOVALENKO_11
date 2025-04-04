


internal class Action
{

    private List<Figure> figures = new List<Figure>();

    private List<List<Figure>> memory = new List<List<Figure>>();

    private Drawer drawer = new Drawer();

    private Backgrounder background = new Backgrounder();  

    private Mover mover = new Mover();

    private FileManager fileManager = new FileManager();

    private Input input = new Input();

    private int index = 0;

    private int memoryIndex = -1;

    private int x = 1;

    private int y = 10;

    private int hight = 208;

    private int width = 49;

    private bool first = true;

    public void Execute(int index)
    {

        if (index == 0) {

            if (figures == null)
            {
                figures = new List<Figure>();
            }

            if (figures.Count < 15)
            {

                while (memoryIndex < memory.Count && memoryIndex > -1)
                {
                    figures = memory[memory.Count - 1];
                    memory.RemoveAt(memory.Count - 1);
                }

                Console.WriteLine("0 - Circle; 1 - Rectangle; 2 - Triangle; 3 - Heart; 4 - Star");

                int choose = input.CorrectInput();

                while (choose < 0 || choose > 4)
                {
                    Console.SetCursorPosition(0, Console.CursorTop - 1);
                    Console.Write(new string(' ', Console.WindowWidth));
                    Console.SetCursorPosition(0, Console.CursorTop);

                    Console.WriteLine("Number must be between 0 and 4");

                    choose = input.CorrectInput();
                }

                int a = 0;
                switch (choose)
                {
                    case 0:
                        Console.WriteLine("Input radius");
                        a = input.CorrectInput();
                        while (a < 2 || a > 24)
                        {
                            Console.SetCursorPosition(0, Console.CursorTop - 1);
                            Console.Write(new string(' ', Console.WindowWidth));
                            Console.SetCursorPosition(0, Console.CursorTop);

                            Console.WriteLine("Number must be between 2 and 24");

                            a = input.CorrectInput();
                        }
                        Console.SetCursorPosition(0, Console.CursorTop - 1);
                        Console.Write(new string(' ', Console.WindowWidth));
                        Console.SetCursorPosition(0, Console.CursorTop);
                        Circle circle = new Circle(a);
                        figures.Add(circle);
                        AddMemory(figures);
                        drawer.Draw(circle);
                        break;
                    case 1:
                        Console.WriteLine("Input height");
                        a = input.CorrectInput();
                        while (a < 2 || a > 48)
                        {
                            Console.SetCursorPosition(0, Console.CursorTop - 1);
                            Console.Write(new string(' ', Console.WindowWidth));
                            Console.SetCursorPosition(0, Console.CursorTop);

                            Console.WriteLine("Number must be between 2 and 48");

                            a = input.CorrectInput();
                        }
                        int b = 0;
                        Console.SetCursorPosition(0, Console.CursorTop - 1);
                        Console.Write(new string(' ', Console.WindowWidth));
                        Console.SetCursorPosition(0, Console.CursorTop);
                        Console.WriteLine("Input whight");
                        b = input.CorrectInput();
                        while (b < 2 || b > 103)
                        {
                            Console.SetCursorPosition(0, Console.CursorTop - 1);
                            Console.Write(new string(' ', Console.WindowWidth));
                            Console.SetCursorPosition(0, Console.CursorTop);

                            Console.WriteLine("Number must be between 2 and 103");

                            b = input.CorrectInput();
                        }
                        Rectangle rectangle = new Rectangle(b, a);
                        Console.SetCursorPosition(0, Console.CursorTop - 1);
                        Console.Write(new string(' ', Console.WindowWidth));
                        Console.SetCursorPosition(0, Console.CursorTop);
                        figures.Add(rectangle);
                        AddMemory(figures);
                        drawer.Draw(rectangle);
                        break;
                    case 2: 
                        Console.WriteLine("Input first side"); 
                        a = input.CorrectInput(); 
                        while (a < 1 || a > 47) 
                        { 
                            Console.SetCursorPosition(0, Console.CursorTop - 1); 
                            Console.Write(new string(' ', Console.WindowWidth)); 
                            Console.SetCursorPosition(0, Console.CursorTop); 
                            Console.WriteLine("Number must be between 1 and 47"); 
                            a = input.CorrectInput(); 
                        } 
                        Console.SetCursorPosition(0, Console.CursorTop - 1); 
                        Console.Write(new string(' ', Console.WindowWidth)); 
                        Console.SetCursorPosition(0, Console.CursorTop); 
                        Console.WriteLine("Input second side"); 
                        int d = input.CorrectInput(); 
                        while (d < 1 || d > 47) 
                        { 
                            Console.SetCursorPosition(0, Console.CursorTop - 1); 
                            Console.Write(new string(' ', Console.WindowWidth)); 
                            Console.SetCursorPosition(0, Console.CursorTop); 
                            Console.WriteLine("Number must be between 1 and 47"); 
                            d = input.CorrectInput(); 
                        } 
                        Console.SetCursorPosition(0, Console.CursorTop - 1); 
                        Console.Write(new string(' ', Console.WindowWidth)); 
                        Console.SetCursorPosition(0, Console.CursorTop); 
                        Console.WriteLine("Input third side"); 
                        int c = input.CorrectInput(); 
                        while (c < 1 || c > 47) 
                        { 
                            Console.SetCursorPosition(0, Console.CursorTop - 1); 
                            Console.Write(new string(' ', Console.WindowWidth)); 
                            Console.SetCursorPosition(0, Console.CursorTop); 
                            Console.WriteLine("Number must be between 1 and 47"); 
                            c = input.CorrectInput(); 
                        } 
                        Console.SetCursorPosition(0, Console.CursorTop - 1); 
                        Console.Write(new string(' ', Console.WindowWidth)); 
                        Console.SetCursorPosition(0, Console.CursorTop);
                        while (a + d <= c || a + c <= d || d + c <= a) 
                        { 
                            Console.WriteLine("Triangle with such sides cannot exist. Enter sides again."); 
                            a = input.CorrectInput(); 
                            b = input.CorrectInput(); 
                            c = input.CorrectInput(); 
                        } 
                        Triangle triangle = new Triangle(a, d, c); 
                        figures.Add(triangle); AddMemory(figures); 
                        drawer.Draw(triangle); 
                        break;
                    case 3:
                        Console.WriteLine("Input size");
                        a = input.CorrectInput();
                        while (a < 2 || a > 11)
                        {
                            Console.SetCursorPosition(0, Console.CursorTop - 1);
                            Console.Write(new string(' ', Console.WindowWidth));
                            Console.SetCursorPosition(0, Console.CursorTop);

                            Console.WriteLine("Number must be between 2 and 11");

                            a = input.CorrectInput();
                        }
                        Console.SetCursorPosition(0, Console.CursorTop - 1);
                        Console.Write(new string(' ', Console.WindowWidth));
                        Console.SetCursorPosition(0, Console.CursorTop);
                        Heart heart = new Heart(a);
                        figures.Add(heart);
                        AddMemory(figures);
                        drawer.Draw(heart);
                        break;
                    case 4:
                        Console.WriteLine("Input size");
                        a = input.CorrectInput();
                        while (a < 2 || a > 24)
                        {
                            Console.SetCursorPosition(0, Console.CursorTop - 1);
                            Console.Write(new string(' ', Console.WindowWidth));
                            Console.SetCursorPosition(0, Console.CursorTop);

                            Console.WriteLine("Number must be between 2 and 24");

                            a = input.CorrectInput();
                        }
                        Console.SetCursorPosition(0, Console.CursorTop - 1);
                        Console.Write(new string(' ', Console.WindowWidth));
                        Console.SetCursorPosition(0, Console.CursorTop);
                        Star star = new Star(a);
                        figures.Add(star);
                        AddMemory(figures);
                        drawer.Draw(star);
                        break;
                }
            }
            else
            {
                Console.WriteLine("Canvas has max count figures. Press key");
                Console.ReadKey();
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);
            }

        }
        else if (index == 1)
        {
            if (figures.Count > 0)
            {

                while (memoryIndex < memory.Count && memoryIndex > -1)
                {
                    figures = memory[memory.Count - 1];
                    memory.RemoveAt(memory.Count - 1);
                }

                ShowList(figures);

                Console.WriteLine("Input number of figure which you wont to erase");

                int choose = input.CorrectInput();

                while (choose < 0 || choose >= figures.Count)
                {
                    Console.SetCursorPosition(0, Console.CursorTop - 1);
                    Console.Write(new string(' ', Console.WindowWidth));
                    Console.SetCursorPosition(0, Console.CursorTop);

                    Console.WriteLine($"Number must be between 0 and {figures.Count - 1}");

                    choose = input.CorrectInput();
                }

                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);

                figures.RemoveAt(choose);
                AddMemory(figures);


                ClearArea(x, y, hight, width);

                foreach (Figure f in figures)
                {
                    drawer.Draw(f);
                    if (f.Back)
                    {
                        background.Background(f, f.Sym);
                    }
                }
            }
            else
            {
                Console.WriteLine("Canvas does not have figures. Press key");
                Console.ReadKey();
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);
            }

        }
        else if (index == 2)
        {
            if (figures.Count > 0)
            {
                while (memoryIndex < memory.Count && memoryIndex > -1)
                {
                    figures = memory[memory.Count - 1];
                    memory.RemoveAt(memory.Count - 1);
                }

                ShowList(figures);

                Console.WriteLine("Input number of figure which you wont to move");

                int choose = input.CorrectInput();

                while (choose < 0 || choose >= figures.Count)
                {
                    Console.SetCursorPosition(0, Console.CursorTop - 1);
                    Console.Write(new string(' ', Console.WindowWidth));
                    Console.SetCursorPosition(0, Console.CursorTop);

                    Console.WriteLine($"Number must be between 0 and {figures.Count - 1}");

                    choose = input.CorrectInput();
                }

                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);


                int move = -1;

                Console.WriteLine("1 - left; 2 - right; 3 - up; 4 - down; 5 - exit");

                while (move != 5)
                {
                    
                    move = input.CorrectInput();

                    int cursor = Console.CursorTop;

                    int count = 0;

                    while (move < 1 || move > 5)
                    {
                        if (count == 1)
                        {
                            Console.SetCursorPosition(0, Console.CursorTop - 1);
                            Console.Write(new string(' ', Console.WindowWidth));
                            Console.SetCursorPosition(0, Console.CursorTop);
                        }

                        Console.WriteLine($"Number must be between 0 and 5");

                        move = input.CorrectInput();

                        count = 1;
                    }

                    if (count == 1)
                    {
                        Console.SetCursorPosition(0, Console.CursorTop - 1);
                        Console.Write(new string(' ', Console.WindowWidth));
                        Console.SetCursorPosition(0, Console.CursorTop);
                    }


                    
                    mover.Move(figures[choose], 1, move);

                    if (move != 5)
                    {
                        AddMemory(figures);
                    }

                    ClearArea(x, y, hight, width);

                    foreach (Figure f in figures)
                    {
                        drawer.Draw(f);
                        if (f.Back)
                        {
                            background.Background(f, f.Sym);
                        }
                    }

                    Console.SetCursorPosition(0, cursor);

                }

                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);
            }
            else
            {
                Console.WriteLine("Canvas does not have figures. Press key");
                Console.ReadKey();
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);
            }
        }
        else if (index == 3)
        {

            while (memoryIndex < memory.Count && memoryIndex > -1)
            {
                figures = memory[memory.Count - 1];
                memory.RemoveAt(memory.Count - 1);
            }

            if (figures.Count > 0)
            {
                ShowList(figures);

                Console.WriteLine("Input number of figure which you want to add a backdroung");

                int choose = input.CorrectInput();

                while (choose < 0 || choose >= figures.Count)
                {
                    Console.SetCursorPosition(0, Console.CursorTop - 1);
                    Console.Write(new string(' ', Console.WindowWidth));
                    Console.SetCursorPosition(0, Console.CursorTop);

                    Console.WriteLine($"Number must be between 0 and {figures.Count - 1}");

                    choose = input.CorrectInput();
                }

                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);

                Console.WriteLine("Input symbol: ");

                string sym = Console.ReadLine();

                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);


                int count = 1;
                
                while (sym.Length != 1)
                {
                    for (int i = 0; i < count; i++)
                    {
                        Console.SetCursorPosition(0, Console.CursorTop - 1);
                        Console.Write(new string(' ', Console.WindowWidth));
                        Console.SetCursorPosition(0, Console.CursorTop);
                    }
                    Console.WriteLine("Input not correct, try again");

                    count = 2;

                    sym = Console.ReadLine();
                }


                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);

                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);

                if (figures[choose] is Circle circle)
                {
                    figures.Add(circle.Clone());
                }
                else if (figures[choose] is Rectangle rectangle)
                {
                    figures.Add(rectangle.Clone());
                }
                else if (figures[choose] is Triangle triangle)
                {
                    figures.Add(triangle.Clone());
                }
                else if (figures[choose] is Heart heart)
                {
                    figures.Add(heart.Clone());
                }
                else if (figures[choose] is Star star)
                {
                    figures.Add(star.Clone());
                }

                background.Background(figures[figures.Count-1], sym[0]);
                figures.RemoveAt(choose);
                AddMemory(figures);


                ClearArea(x, y, hight, width);

                foreach (Figure f in figures)
                {
                    drawer.Draw(f);
                    if (f.Back)
                    {
                        background.Background(f, f.Sym);
                    }
                }
            }
            else
            {
                Console.WriteLine("Canvas does not have figures. Press key");
                Console.ReadKey();
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, Console.CursorTop);
            }
        }
        else if (index == 4)
        {
            if (figures != null && figures.Count > 0)
            {

                List<Figure> clone = new List<Figure>();

                foreach (Figure f in figures)
                {
                    if (f is Circle circle)
                    {
                        clone.Add(circle.Clone());
                    }
                    else if (f is Rectangle rectangle)
                    {
                        clone.Add(rectangle.Clone());
                    }
                    else if (f is Triangle triangle)
                    {
                        clone.Add(triangle.Clone());
                    }
                    else if (f is Heart heart)
                    {
                        clone.Add(heart.Clone());
                    }
                    else if (f is Star star)
                    {
                        clone.Add(star.Clone());
                    }
                }

                fileManager.InputFile(clone);

                memoryIndex = -1;

                memory = new List<List<Figure>>();
            }
        }
        else if (index == 5)
        {


            figures = fileManager.OutputFile();
            

            if (figures != null && figures.Count > 0)
            {

                AddMemory(figures);
                foreach (Figure f in figures)
                {
                    drawer.Draw(f);
                    if (f.Back)
                    {
                        background.Background(f, f.Sym);
                    }
                }
            }
            else
            {
                ClearArea(x, y, hight, width);
            }

        }
        else if (index == 6)
        {
            Undo();
        }
        else if (index == 7)
        {
            Redo();
        }
        else if (index == 8)
        {
            Environment.Exit(0);
        }


    }


    private void AddMemory(List<Figure> figures)
    {
        if (memoryIndex < 10)
        {
            memoryIndex++;
        }
        
        while(memoryIndex < memory.Count) {
            figures = memory[memory.Count - 1];
            memory.RemoveAt(memory.Count-1);
        }

        List<Figure> clone = new List<Figure>();

        foreach (Figure f in figures)
        {
            if (f is Circle circle)
            {
                clone.Add(circle.Clone());
            }
            else if (f is Rectangle rectangle)
            {
                clone.Add(rectangle.Clone());
            }
            else if (f is Triangle triangle)
            {
                clone.Add(triangle.Clone());
            }
            else if (f is Heart heart)
            {
                clone.Add(heart.Clone());
            }
            else if (f is Star star)
            {
                clone.Add(star.Clone());
            }
        }

        memory.Add(clone);

        if (memory.Count > 10) {
            memory.RemoveAt(0);
            first = false;
        }
    }

    private void ClearArea(int x, int y, int width, int height)
    {
        for (int i = 0; i < height; i++)
        {
            Console.SetCursorPosition(x, y + i);
            Console.Write(new string(' ', width));
        }

        Console.SetCursorPosition(x, y);
    }

    private void Undo()
    {

         if (memoryIndex >= 0)
        {
            if (first)
            {
                ClearArea(x, y, hight, width);
            }
            else
            {
                if (memoryIndex > 0)
                {
                    ClearArea(x, y, hight, width);
                }
                
            }

            memoryIndex--;

            if (memoryIndex == 9)
            {
                memoryIndex--;
            }

            if (memoryIndex >= 0)
            {

                foreach (Figure f in memory[memoryIndex])
                {
                    drawer.Draw(f);
                    if (f.Back)
                    {
                        background.Background(f, f.Sym);
                    }
                }
            }

        }
        else
        {
            memoryIndex = -1;
        }



    }


    private void Redo()
    {

        if (memoryIndex < memory.Count && memory.Count > 0)
        {
            ClearArea(x, y, hight, width);

            if (memoryIndex + 1 <= memory.Count - 1)
            {
                memoryIndex++;
            }

            foreach (Figure f in memory[memoryIndex])
            {
                drawer.Draw(f);
                if (f.Back)
                {
                    background.Background(f, f.Sym);
                }
            }

            
            
        }

    }

    private void ShowList(List<Figure> figures)
    {
        int i = 0;

        foreach (Figure f in figures)
        {
            if (f is Circle circle)
            {
                Console.Write($"{i}. Circle ");
            }
            else if (f is Rectangle rectangle)
            {
                Console.Write($"{i}. Rectangle ");
            }
            else if (f is Triangle triangle)
            {
                Console.Write($"{i}. Triangle ");
            }
            else if (f is Heart heart)
            {
                Console.Write($"{i}. Heart ");
            }
            else if (f is Star star)
            {
                Console.Write($"{i}. Star ");
            }

            ++i;

            if (i % 5 == 0)
            {
                Console.WriteLine();
            }
        }

        if (i % 5 != 0)
        {
            Console.WriteLine();
        }
    }
} 