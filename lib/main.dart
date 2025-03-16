import 'package:flutter/material.dart';
import 'pages/login.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Skin Tracking App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.red,
          primary: Colors.white,
          secondary: Colors.blueGrey,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      home: const LoginPage(),
    );
  }
}