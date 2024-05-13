@main
def oop_domain_modeiling(): Unit ={

  // traits and classes are two main tools for data encapsulation
  // Class
  class Person(var firstName: String, var lastName: String):
    def printFullName() = println(s"$firstName $lastName")


  val p = Person("Kalyan", "Adhikari")
  println(p.firstName)
  p.printFullName()

//  traits

  


}