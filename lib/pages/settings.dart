import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class Settings extends StatefulWidget {
  const Settings({super.key});

  @override
  _SettingsState createState() => _SettingsState();
}

class _SettingsState extends State<Settings> {
  bool isDarkMode = false;
  double fontSize = 16.0;

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      isDarkMode = prefs.getBool('isDarkMode') ?? false;
      fontSize = prefs.getDouble('fontSize') ?? 16.0;
    });
  }

  Future<void> _saveSettings() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isDarkMode', isDarkMode);
    await prefs.setDouble('fontSize', fontSize);
  }

  Future<void> clearLocalStorage() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear(); // Clears all stored data
    setState(() {}); // refresh UI after clearing data
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Settings"),
        backgroundColor: Colors.red[300],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const Text(
              "Settings Page",
              style: TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 30),

            // 🔲 Dark Mode Switch
            SwitchListTile(
              title: const Text("Dark Mode"),
              value: isDarkMode,
              onChanged: (value) {
                setState(() {
                  isDarkMode = value;
                });
                _saveSettings();
              },
            ),

            const SizedBox(height: 20),

            // Font Size Slider
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text("Font Size"),
                Slider(
                  value: fontSize,
                  min: 12,
                  max: 30,
                  divisions: 9,
                  label: fontSize.toStringAsFixed(0),
                  onChanged: (value) {
                    setState(() {
                      fontSize = value;
                    });
                    _saveSettings();
                  },
                ),
              ],
            ),

            const SizedBox(height: 30),

            //  Reset Data Button
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
