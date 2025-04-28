import 'dart:io';
import 'dart:math';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:skinsensor2025/componenets/nav_bar.dart';
import 'package:skinsensor2025/services/tf_service.dart';
import 'package:skinsensor2025/componenets/scan_records.dart';

class ScanningPage extends StatefulWidget {
  const ScanningPage({super.key});
  @override
  State<ScanningPage> createState() => _ScanningPageState();
}

class _ScanningPageState extends State<ScanningPage> {
  final _picker = ImagePicker();
  final _tf = TFLiteService();

  File? selectedImage;
  bool isScanning = false;
  String scanResult = "";
  Map<String, dynamic> skinInfo = {};

  @override
  void initState() {
    super.initState();
    _tf.loadModel();
    _loadSkinInfo();
  }

  Future<void> _loadSkinInfo() async {
    final data = await DefaultAssetBundle.of(context).loadString(
        'assets/skin_conditions.json');
    setState(() {
      skinInfo = Map<String, dynamic>.from(json.decode(data));
    });
  }

  Future<void> _saveScan(ScanRecord record) async {
    final prefs = await SharedPreferences.getInstance();
    final existing = prefs.getString('scan_history') ?? '[]';
    final list = ScanRecord.decodeList(existing);
    list.insert(0, record);
    await prefs.setString('scan_history', ScanRecord.encodeList(list));
  }

  Future<void> pickImageFromGallery() async {
    final XFile? img = await _picker.pickImage(source: ImageSource.gallery);
    if (img != null) {
      setState(() {
        selectedImage = File(img.path);
        scanResult = "";
      });
    }
  }

  Future<void> pickImageFromCamera() async {
    final XFile? img = await _picker.pickImage(source: ImageSource.camera);
    if (img != null) {
      setState(() {
        selectedImage = File(img.path);
        scanResult = "";
      });
    }
  }

  Future<void> startScanning() async {
    if (selectedImage == null) {
      setState(() => scanResult = "Please select an image first.");
      return;
    }

    setState(() {
      isScanning = true;
      scanResult = "";
    });

    try {
      final bytes = await selectedImage!.readAsBytes();
      final output = await _tf.runInference(bytes);

      final pairs = <MapEntry<String, double>>[];
      for (var i = 0; i < output.length; i++) {
        final label = _tf.labels[i]!;
        pairs.add(MapEntry(label, output[i]));
      }
      pairs.sort((a, b) => b.value.compareTo(a.value));

      final best = pairs.first;
      final confidencePct = best.value * 100.0;

      // Save to history
      final rec = ScanRecord(
        imagePath: selectedImage!.path,
        label: best.key,
        confidence: confidencePct,
        timestamp: DateTime.now(),
      );
      await _saveScan(rec);


      final condition = skinInfo[best.key];
      final description = condition?['description'] ??
          "No description available.";
      final treatmentsList = condition?['treatments'] as List<dynamic>? ?? [];
      final treatments = treatmentsList.map((t) => "- ${t['name']}").join("\n");

      setState(() {
        isScanning = false;
        scanResult =
        "Diagnosis: ${best.key} (${confidencePct.toStringAsFixed(1)}%)\n\n"
            "Description:\n$description\n\n"
            "Recommended Treatments:\n$treatments\n\n"
            "Disclaimer: This diagnosis is AI-generated and may not be 100% accurate. Please consult a qualified medical professional.";
      });
    } catch (e) {
      setState(() {
        isScanning = false;
        scanResult = "Error running model:\n$e";
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
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Image Preview
                Container(
                  height: 400,
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: Colors.grey[300],
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: selectedImage != null
                      ? Image.file(selectedImage!, fit: BoxFit.cover)
                      : const Center(
                    child: Text(
                      "No Image Selected",
                      style: TextStyle(color: Colors.black54),
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // Diagnosis Result
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
                          color: Colors.black, fontWeight: FontWeight.bold),
                      textAlign: TextAlign.left,
                    ),
                  ),

                const SizedBox(height: 16),

                // Gallery & Camera buttons
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

                // Start Scan button
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
        ),
      ),
      bottomNavigationBar: const NavBar(currentIndex: 1),
    );
  }
}
