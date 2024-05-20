//@main def hello() = println("hello world")

import  scala.io.StdIn.readLine
//There are several ways to read input from a command-line, but a simple way is to use the readLine method in the scala.io.StdIn object

@main def helloInteractive(): Unit =
  println("Please enter your name :")
  val name = readLine()

  println("hello" + name + "!")
