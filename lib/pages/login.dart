import 'package:flutter/material.dart';
import 'package:skinsensor2025/componenets/login_button.dart';
import 'package:skinsensor2025/componenets/text_field.dart';
import 'package:skinsensor2025/pages/home.dart'; //
class LoginPage extends StatefulWidget{
  const LoginPage ({super.key});


  @override
  State<LoginPage> createState() => _LoginPageState();
}

  class _LoginPageState extends State<LoginPage>{

  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey,

      body: Center(
        child: Padding(padding: const EdgeInsets.symmetric(horizontal:25.0),
        child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [

            Padding(
              padding: const EdgeInsets.all(40.0),
              child: Image.asset('lib/images/holder.jpg', height: 240,
              ),
            ),

              const SizedBox(height: 48,),
            
               Text('Start your journey ',
               style: TextStyle(
                   fontWeight: FontWeight.bold,
                 fontSize: 20,
               ),
            ),
              const SizedBox(height: 48,),

            MyTextField(controller: emailController
                , hinText: 'enter email',
                obscureText: false),

            const SizedBox(height: 15,),

            MyTextField(controller: passwordController
                , hinText: 'true',
                obscureText: false),

             const SizedBox(height: 15,),

            Align (
               alignment: Alignment.centerRight,
              child: Text(
                'forgot password?',
                style: TextStyle(
                    color: Theme.of(context).colorScheme.primary,
                fontWeight: FontWeight.bold,
                ),
              ),

            ),
            
            const SizedBox(height: 15,),   
            
            Mybutton(text: "Login",
                onTap: (){

                  // Navigate to HomePage when login button is pressed
                  Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                      builder: (context) => const HomePage(),

                      ),
                  );

                }

            ),
            
             const SizedBox(height: 30,),
            
            Text("Register Now")
                                                                           


          ],                                  
        ),
      ),
    ),
    ),
    );
  }
}


