




public class Backgrounder
{

    char sym = '.';

    public void SetSymbol(char sym)
    {
        this.sym = sym;
    }

    public void Background(Figure figure)
    {
        if (figure is Circle circle)
        {
            BackCircle(circle);
        }
        else if (figure is Rectangle rectangle)
        {
            BackRectangle(rectangle);
        }
        else if (figure is Triangle triangle)
        {
            BackTriangle(triangle);
        }
        else if (figure is Heart heart)
        {
            BackHeart(heart);
        }
        else if (figure is Star star)
        {
            BackStar(star);
        }
    }


    public void Background(Figure figure, char sym)
    {

        this.sym = sym;
        

        if (figure is Circle circle)
        {
            BackCircle(circle);
        }
        else if (figure is Rectangle rectangle)
        {
            BackRectangle(rectangle);
        }
        else if (figure is Triangle triangle)
        {
            BackTriangle(triangle);
        }
        else if (figure is Heart heart)
        {
            BackHeart(heart);
        }
        else if (figure is Star star)
        {
            BackStar(star);
        }
    }


    private void BackCircle(Circle circle)
    {

        circle.Sym = sym;
        circle.Back = true;

        for (int y = -circle.A; y <= circle.A; y++)
        {
            for (int x = -circle.A * 2; x <= circle.A * 2; x += 1)
            {

                double distance = Math.Sqrt((x / 2) * (x / 2) + y * y);

                if (distance < circle.A-0.51)
                {
                    Console.SetCursorPosition(circle.X + x, circle.Y + y);
                    Console.WriteLine(circle.Sym);

                }
            }
        }

    }

    private void BackRectangle(Rectangle rectangle)
    {

        rectangle.Sym = sym;
        rectangle.Back = true;

        for (int x = -rectangle.A+1; x <= rectangle.A-1; x += 1)
        {
            for (int y = -rectangle.B / 2+1; y <= rectangle.B - rectangle.B / 2-1; y++)
            {
                Console.SetCursorPosition(rectangle.X + x, rectangle.Y + y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(rectangle.X - x, rectangle.Y + y);
                Console.WriteLine(sym);
            }
        }

    }


    private void BackTriangle(Triangle triangle)
    {
        triangle.Sym = sym;
        triangle.Back = true;

        int c = triangle.C; 
        int a = triangle.A; 
        int d = triangle.D; 

        double p = (a + d + c) / 2.0;
        double area = Math.Sqrt(p * (p - a) * (p - d) * (p - c));
        double h = (2 * area) / c; 

        double g = (a * a - d * d + c * c) / (2.0 * c);

        int x0 = triangle.X; 
        int y0 = triangle.Y;
        int apexX = (int)(x0 + g); 
        int apexY = (int)(y0 - h);
        int rightX = x0 + c;

        for (int y = y0-1; y >= apexY; y--)
        {
            int leftX = FindXOnLine(x0, y0, apexX, apexY, y);

            int right1X = FindXOnLine(rightX, y0, apexX, apexY, y);

            for (int x = leftX+1; x <= right1X-1; x++)
            {
                Console.SetCursorPosition(x, y);
                Console.Write(sym);
            }
        }
    }

    private int FindXOnLine(int x0, int y0, int x1, int y1, int targetY)
    {
        int dx = Math.Abs(x1 - x0);
        int dy = Math.Abs(y1 - y0);
        int sx = x0 < x1 ? 1 : -1;
        int sy = y0 < y1 ? 1 : -1;
        int err = dx - dy;

        int x = x0;
        int y = y0;

        while (true)
        {
            if (y == targetY) return x; 

            if (x == x1 && y == y1) break; 

            int e2 = 2 * err;
            if (e2 > -dy)
            {
                err -= dy;
                x += sx;
            }
            if (e2 < dx)
            {
                err += dx;
                y += sy;
            }
        }

        return x; 
    }



    private void BackHeart(Heart heart)
    {

        heart.Sym = sym;
        heart.Back = true;

        int x = 0;

        for (int y = heart.A; y < 2 * heart.A; y++)
        {

            for (int i = x+4; i < 4*heart.A-x; i += 1) {


                Console.SetCursorPosition(heart.X - i, heart.Y - y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(heart.X + i, heart.Y - y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(heart.X - 4 * heart.A + i, heart.Y - y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(heart.X + 4 * heart.A - i, heart.Y - y);
                Console.WriteLine(sym);

            }
            x += 2;
        }



        Console.SetCursorPosition(heart.X - x, heart.Y - 2 * heart.A + 1);
        Console.WriteLine(".");
        Console.SetCursorPosition(heart.X + x, heart.Y - 2 * heart.A + 1);
        Console.WriteLine(".");

        for (int i = 0; i <= heart.A; i++)
        {
            for (int j = 1; j < 4 * heart.A+2; j += 1)
            {
                Console.SetCursorPosition(heart.X - 4 * heart.A+j, heart.Y - heart.A + i);
                Console.WriteLine(sym);
                Console.SetCursorPosition(heart.X + 4 * heart.A-j, heart.Y - heart.A + i);
                Console.WriteLine(sym);
            }
        }


        for (int y = 1; y <= 2 * heart.A + 1; y++)
        {
            for (int i = 0; i < x*2; i += 1)
            {
                Console.SetCursorPosition(heart.X  - i, heart.Y + y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(heart.X + i, heart.Y + y);
                Console.WriteLine(sym);
            }
            x -= 1;
        }

        Console.SetCursorPosition(heart.X, heart.Y-heart.A);
        Console.WriteLine('.');
    }

    private void BackStar(Star star)
    {

        star.Sym = sym;
        star.Back = true;

        int x = 0;
        int y = star.A;

        while (y >= x / 2)
        {

            for (int i = 0; i < x; i += 1)
            {
                Console.SetCursorPosition(star.X + i, star.Y + y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(star.X - i, star.Y + y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(star.X + i, star.Y - y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(star.X - i, star.Y - y);
                Console.WriteLine(sym);
            }
     
            x += 1;
            y -= 1;

        }

        if (y < x / 2)
        {

            for (int i = 0; i < x; i+= 1)
            {
                for (int j = 0; j <= y; j++)
                {
                    Console.SetCursorPosition(star.X + i, star.Y + j);
                    Console.WriteLine(sym);
                    Console.SetCursorPosition(star.X - i, star.Y + j);
                    Console.WriteLine(sym);
                    Console.SetCursorPosition(star.X + i, star.Y - j);
                    Console.WriteLine(sym);
                    Console.SetCursorPosition(star.X - i, star.Y - j);
                    Console.WriteLine(sym);
                }
            }

            
        }

       


        while (x < 2 * star.A)
        {

            for (int i = 0; i <= x; i += 1)
            {
                Console.SetCursorPosition(star.X + i, star.Y + y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(star.X - i, star.Y + y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(star.X + i, star.Y - y);
                Console.WriteLine(sym);
                Console.SetCursorPosition(star.X - i, star.Y - y);
                Console.WriteLine(sym);
            }

            x += 4;

            y--;
            

        }

    }


}
