

public class Heart : Figure
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

    public Heart(int a)
    {
        A = a;
    }

    public Heart Clone()
    {
        return new Heart(a)
        {
            X = this.X,
            Y = this.Y,
            Sym = this.Sym,
            Back = this.Back
        };
    }
}