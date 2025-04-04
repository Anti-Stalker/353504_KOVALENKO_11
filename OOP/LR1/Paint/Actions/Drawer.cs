


using System.Security.Cryptography;

internal class Drawer
{
    public void Draw(Figure figure)
    {
        if (figure is Circle circle)
        {
            DrawCircle(circle);
        }
        else if (figure is Rectangle rectangle) 
        {
            DrawRectangle(rectangle);
        }
        else if (figure is Triangle triangle)
        {
            DrawTriangle(triangle);
        }
        else if (figure is Heart heart)
        {
            DrawHeart(heart);
        }
        else if (figure is Star star)
        {
            DrawStar(star);
        }
    }


    private void DrawCircle(Circle circle)
    {

        for (int y = -circle.A; y <= circle.A; y++)
        {
            for (int x = -circle.A*2; x <= circle.A*2; x += 2)
            {
                   
                double distance = Math.Sqrt((x/2) * (x/2) + y * y);

                if (Math.Abs(distance - circle.A) < 0.5)
                {
                    Console.SetCursorPosition(circle.X+x, circle.Y+y);
                    Console.WriteLine('о');
          
                }
            }
        }

    }

    private void DrawRectangle(Rectangle rectangle)
    {

        for (int x = -rectangle.A; x <= rectangle.A; x += 2)
        {
            Console.SetCursorPosition(rectangle.X + x, rectangle.Y - rectangle.B/2);
            Console.WriteLine('о');
            Console.SetCursorPosition(rectangle.X + x, rectangle.Y + rectangle.B - rectangle.B / 2);
            Console.WriteLine('о');
        }


        for (int y = -rectangle.B/2;  y <= rectangle.B - rectangle.B/2; y++)
        {
            Console.SetCursorPosition(rectangle.X + rectangle.A, rectangle.Y + y);
            Console.WriteLine('о');
            Console.SetCursorPosition(rectangle.X - rectangle.A, rectangle.Y + y);
            Console.WriteLine('о');
        }

    }


    private void DrawTriangle(Triangle triangle)
    {
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

        for (int x = x0; x <= x0 + c; x++)
        {
            Console.SetCursorPosition(x, y0);
            Console.Write('о');
        }

        DrawLine(x0, y0, apexX, apexY);

        DrawLine(x0 + c, y0, apexX, apexY);
    }

    private void DrawLine(int x0, int y0, int x1, int y1)
    {
        int dx = Math.Abs(x1 - x0);
        int dy = Math.Abs(y1 - y0);
        int sx = x0 < x1 ? 1 : -1;
        int sy = y0 < y1 ? 1 : -1;
        int err = dx - dy;

        while (true)
        {
            Console.SetCursorPosition(x0, y0);
            Console.Write('о');

            if (x0 == x1 && y0 == y1) break;
            int e2 = 2 * err;
            if (e2 > -dy)
            {
                err -= dy;
                x0 += sx;
            }
            if (e2 < dx)
            {
                err += dx;
                y0 += sy;
            }
        }
    }



    private void DrawHeart(Heart heart)
    {
        int x = 0;

        for(int y = heart.A; y < 2*heart.A; y++)
        {
            Console.SetCursorPosition(heart.X - x, heart.Y - y);
            Console.WriteLine("о");
            Console.SetCursorPosition(heart.X + x, heart.Y - y);
            Console.WriteLine("о");
            Console.SetCursorPosition(heart.X - 4*heart.A + x, heart.Y - y);
            Console.WriteLine("о");
            Console.SetCursorPosition(heart.X + 4*heart.A - x, heart.Y - y);
            Console.WriteLine("о");
            x += 2;
        }
           
        Console.SetCursorPosition(heart.X - x, heart.Y - 2*heart.A+1);
        Console.WriteLine("о");
        Console.SetCursorPosition(heart.X + x, heart.Y -2 * heart.A + 1);
        Console.WriteLine("о");

        for (int i = 0; i <= heart.A; i++)
        {
            Console.SetCursorPosition(heart.X - 4 * heart.A, heart.Y - heart.A+i);
            Console.WriteLine("о");
            Console.SetCursorPosition(heart.X + 4 * heart.A, heart.Y - heart.A  +i);
            Console.WriteLine("о");
        }


        for (int y = 1; y <= 2*heart.A+1; y++)
        {
            Console.SetCursorPosition(heart.X - 2*heart.A - x, heart.Y + y);
            Console.WriteLine("о");
            Console.SetCursorPosition(heart.X + 2 * heart.A + x, heart.Y + y);
            Console.WriteLine("о");
            x -= 2;
        }
    }

    private void DrawStar(Star star)
    {
        
        int x = 0;
        int y = star.A;

        while (y > x/2)
        {
            Console.SetCursorPosition(star.X + x, star.Y + y);
            Console.WriteLine("о");
            Console.SetCursorPosition(star.X - x, star.Y + y);
            Console.WriteLine("о");
            Console.SetCursorPosition(star.X + x, star.Y - y);
            Console.WriteLine("о");
            Console.SetCursorPosition(star.X - x, star.Y - y);
            Console.WriteLine("о");

            x += 2;
            y -= 2;

        }

       
        if (y < x / 2)
        {
            y++;
            Console.SetCursorPosition(star.X + x, star.Y + y);
            Console.WriteLine("о");
            Console.SetCursorPosition(star.X - x, star.Y + y);
            Console.WriteLine("о");
            Console.SetCursorPosition(star.X + x, star.Y - y);
            Console.WriteLine("о");
            Console.SetCursorPosition(star.X - x, star.Y - y);
            Console.WriteLine("о");
            y--;
            if ((star.A - 7)%3 == 0)
            {
                x += 4;
            }
            else
            {
                x += 2;
            }
            
          
        }

        while(x <= 2 * star.A)
        {
            Console.SetCursorPosition(star.X + x, star.Y + y);
            Console.WriteLine("о");
            Console.SetCursorPosition(star.X - x, star.Y + y);
            Console.WriteLine("о");
            Console.SetCursorPosition(star.X + x, star.Y - y);
            Console.WriteLine("о");
            Console.SetCursorPosition(star.X - x, star.Y - y);
            Console.WriteLine("о");
            y--;
            x += 4;
        }

    }

}