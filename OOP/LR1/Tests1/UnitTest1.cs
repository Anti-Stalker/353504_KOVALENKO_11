

namespace Tests1
{
    public class UnitTest1
    {
        [Test]

        public void Test1()
        {
            FileManager f = new FileManager();

            List <Figure> l=f.OutputFile();
            Assert.IsTrue(l is null);
        }

        [Test]

        public void Test2()
        {
            Mover move = new Mover();

            Circle circle = new Circle(5);

            Assert.IsTrue(move.CheckX(circle, 100) == false);
        }

        [Test]
        public void Test3()
        {
            Mover move = new Mover();

            Circle circle = new Circle(5);

            Assert.IsTrue(move.CheckX(circle, -100) == false);
        }

        [Test]
        public void Test4()
        {
            Mover move = new Mover();

            Circle circle = new Circle(5);

            Assert.IsTrue(move.CheckX(circle, 20) == true);
        }

        [Test]
        public void Test5()
        {
            Mover move = new Mover();

            Circle circle = new Circle(5);

            Assert.IsTrue(move.CheckX(circle, -20) == true);
        }

        [Test]
        public void Test6()
        {
            Mover move = new Mover();

            Rectangle circle = new Rectangle(5, 5);

            Assert.IsTrue(move.CheckX(circle, 100) == false);
        }

        [Test]
        public void Test7()
        {
            Mover move = new Mover();

            Rectangle circle = new Rectangle(5, 5);

            Assert.IsTrue(move.CheckX(circle, -100) == false);
        }

        [Test]
        public void Test8()
        {
            Mover move = new Mover();

            Rectangle circle = new Rectangle(5, 5);

            Assert.IsTrue(move.CheckY(circle, 100) == false);
        }

        [Test]
        public void Test9()
        {
            Mover move = new Mover();

            Rectangle circle = new Rectangle(5, 5);

            Assert.IsTrue(move.CheckY(circle, 100) == false);
        }

        [Test]
        public void Test10()
        {
            Mover move = new Mover();

            Triangle circle = new Triangle(5);

            Assert.IsTrue(move.CheckY(circle, 5) == true);
        }

        [Test]
        public void Test11()
        {
            Mover move = new Mover();

            Triangle circle = new Triangle(5);

            Assert.IsTrue(move.CheckY(circle, -5) == true);
        }
    }
}