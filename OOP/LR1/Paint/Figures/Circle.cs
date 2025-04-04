

public class Circle : Figure
{
    private int a = 0;

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

    public Circle(int a)
    {
        A = a; 
    }

    public Circle Clone()
    {
        return new Circle(a)
        {
            X = this.X,
            Y = this.Y,
            Sym = this.Sym,
            Back = this.Back
        };
    }
}