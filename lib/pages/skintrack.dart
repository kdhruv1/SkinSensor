import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:skinsensor2025/componenets/nav_bar.dart';
import 'dart:io';

class ScanningPage extends StatefulWidget {
  const ScanningPage({super.key});

  @override
  State<ScanningPage> createState() => _ScanningPageState();
}

class _ScanningPageState extends State<ScanningPage> {
  bool isScanning = false;
  String scanResult = "";
  File? selectedImage; // Holds the selected image from the gallery or camera

  final ImagePicker _picker = ImagePicker();

  void startScanning() {
    if (selectedImage == null) {
      setState(() {
        scanResult = "Please select an image first.";
      });
      return;
    }

    setState(() {
      isScanning = true;
      scanResult = ""; // Clear previous results
    });

    // Simulate scanning process with a delay
    Future.delayed(const Duration(seconds: 3), () {
      setState(() {
        isScanning = false;
        scanResult = "Potential skin issue detected. Consult a dermatologist.";
      });
    });
  }

  Future<void> pickImageFromGallery() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      setState(() {
        selectedImage = File(image.path);
        scanResult = ""; // Clear any existing scan results
      });
    }
  }

  Future<void> pickImageFromCamera() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.camera);
    if (image != null) {
      setState(() {
        selectedImage = File(image.path);
        scanResult = ""; // Clear any existing scan results
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Skin Tracker Scanner"),
        backgroundColor: Colors.red[300],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            // Displays an selected image or camera preview placeholder
            Container(
              height: 400,
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.circular(12),
              ),
              child: selectedImage != null
                  ? Image.file(
                selectedImage!,
                fit: BoxFit.cover,
              )
                  : const Center(
                child: Text(
                  "No Image Selected",
                  style: TextStyle(color: Colors.black54),
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Scan result section
            if (scanResult.isNotEmpty)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.green[100],
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  scanResult,
                  style: const TextStyle(
                    color: Colors.black,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),

            const Spacer(),

            // Gallery and Camera buttons
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton.icon(
                  onPressed: pickImageFromGallery,
                  icon: const Icon(Icons.photo),
                  label: const Text("Gallery"),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red[300],
                    minimumSize: const Size(150, 50),
                  ),
                ),
                ElevatedButton.icon(
                  onPressed: pickImageFromCamera,
                  icon: const Icon(Icons.camera_alt),
                  label: const Text("Camera"),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red[300],
                    minimumSize: const Size(150, 50),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Scan button
            ElevatedButton.icon(
              onPressed: isScanning ? null : startScanning,
              icon: const Icon(Icons.search),
              label: Text(isScanning ? "Scanning..." : "Start Scan"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red[300],
                minimumSize: const Size(double.infinity, 50),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: const NavBar(currentIndex: 1),
    );

  }
}
