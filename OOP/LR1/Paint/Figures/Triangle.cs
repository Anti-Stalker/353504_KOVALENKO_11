

public class Triangle : Figure
{

    private int a = 0;
    private int d = 0;
    private int c = 0;

    public int A
    {
        get
        {
            return a;
        }

        set
        {
            a = value;
        }
    }
    public int D
    {
        get
        {
            return d;
        }

        set
        {
            d = value;
        }
    }
    public int C
    {
        get
        {
            return c;
        }

        set
        {
            c = value;
        }
    }

    public Triangle(int a, int d, int c)
    {
        A = a;
        D = d;
        C = c;
    }

    public Triangle Clone()
    {
        return new Triangle(a, d, c)
        {
            X = this.X,
            Y = this.Y,
            Sym = this.Sym,
            Back = this.Back
        };
    }

}