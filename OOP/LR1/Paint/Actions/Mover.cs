


public class Mover
{

    public void Move(Figure figure, int x, int index)
    {

        switch (index)
        {
            case 1:
                if (CheckX(figure, -x))
                {
                    figure.X -= x;
                }
                break;
            case 2:
                if (CheckX(figure, x))
                {
                    figure.X += x;
                }
                break;
            case 3:
                if (CheckY(figure, -x))
                {
                    figure.Y -= x;
                }
                break;
            case 4:
                if (CheckY(figure, x))
                {
                    figure.Y += x;
                }
                break;
        }
    }

    public bool CheckX(Figure figure, int a)
    {
        if (figure is Circle circle)
        {
            if (a < 0)
            {
                if (circle.X - 2*circle.A + a > 1)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (circle.X + 2 * circle.A + a < 209)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }
        else if (figure is Rectangle rectangle)
        {
            if (a < 0)
            {
                if (rectangle.X - rectangle.A + a > 1)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (rectangle.X + rectangle.A + a < 209)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }
        else if (figure is Triangle triangle)
        {
            if (a < 0)
            {
                if (triangle.X - triangle.C / 2 + a > 1) // Учитываем половину основания
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (triangle.X + triangle.C / 2 + a < 209)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }
        else if (figure is Heart heart)
        {
            if (a < 0)
            {
                if (heart.X - 4 * heart.A + a > 1)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (heart.X + 4 * heart.A + a < 209)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }
        else if (figure is Star star)
        {
            if (a < 0)
            {
                if (star.X - 2 * star.A + a > 1)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (star.X + 2 * star.A + a < 209)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }

        return false;
    }

    public bool CheckY(Figure figure, int a)
    {
        if (figure is Circle circle)
        {
            if (a < 0)
            {
                if (circle.Y - circle.A + a > 9)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (circle.Y + circle.A + a < 59)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }
        else if (figure is Rectangle rectangle)
        {
            if (a < 0)
            {
                if (rectangle.Y - rectangle.B/2 + a > 9)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (rectangle.Y + rectangle.B - rectangle.B/2 + a < 59)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }
        else if (figure is Triangle triangle)
        {
            double p = (triangle.A + triangle.D + triangle.C) / 2.0;
            double area = Math.Sqrt(p * (p - triangle.A) * (p - triangle.D) * (p - triangle.C));
            double height = (2 * area) / triangle.C;

            if (a < 0)
            {
                if (triangle.Y - (int)height + a > 9)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (triangle.Y + a < 59)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }
        else if (figure is Heart heart)
        {
            if (a < 0)
            {
                if (heart.Y - 2*heart.A+1 + a > 9)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (heart.Y + 2*heart.A +1 + a < 59)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }
        else if (figure is Star star)
        {
            if (a < 0)
            {
                if (star.Y - star.A + a > 9)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                if (star.Y + star.A + a < 59)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }

        return false;
    }
}