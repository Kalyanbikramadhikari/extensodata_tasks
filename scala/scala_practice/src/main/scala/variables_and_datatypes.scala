

@main def datatypes(): Unit ={

  // Creates an immutable variable
  val a = 0

  // Creates a mutable variable
  var b = 1


  // Declaring variable types
  val x: Int = 1 // this is explictly declaring the type by ourself
  val y = 1 // implict, the complier inferss the data type


  val s = "a string"
  val st: String = "a string"

  //val nums = List(1, 2, 3)
  val num: List[Int] = List(1, 2, 3)

  val firstName = "John"
  val mi = 'C'
  val lastName = "Doe"

  println(s"Name: $firstName $mi $lastName")

}
  
