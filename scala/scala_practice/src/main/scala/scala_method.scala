

@main
def scala_methods(): Unit = {

  def sum(a: Int, b:Int): Int = {
    a + b
  }

  def makeConnection(url: String, timeout: Int = 5000): Unit =
    println(s"url=$url, timeout=$timeout")


  val total = sum(2,5)
  println(total)

  makeConnection("https://localhost", 2500)




}
