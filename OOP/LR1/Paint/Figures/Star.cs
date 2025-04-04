

public class Star : Figure
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

    public Star(int a)
    {
        A = a;
    }

    public Star Clone()
    {
        return new Star(a)
        {
            X = this.X,
            Y = this.Y,
            Sym = this.Sym,
            Back = this.Back
        };
    }
}