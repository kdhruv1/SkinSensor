import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class Settings extends StatefulWidget {
  const Settings({super.key});

  @override
  _SettingsState createState() => _SettingsState();
}

class _SettingsState extends State<Settings> {
  //clear storage for testing
  Future<void> clearLocalStorage() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.clear(); // Clears all stored data
    print("Local storage cleared!");
    setState(() {}); // Refresh UI after clearing data
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Settings"),
        backgroundColor: Colors.red[300],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Settings Page",
              style: TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 20),

            // ✅ Button to Clear Local Storage
            ElevatedButton(
              onPressed: () async {
                await clearLocalStorage();
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red[300],
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                textStyle: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              child: const Text("Reset Data"),
            ),
          ],
        ),
      ),
    );
  }
}
