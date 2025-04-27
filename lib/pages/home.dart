import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:skinsensor2025/componenets/nav_bar.dart';
import 'package:skinsensor2025/componenets/scan_records.dart';
import 'package:skinsensor2025/pages/settings.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {

  Map<String, dynamic> conditionInfo = {};
  List<String> classNames = [];

  List<ScanRecord> _history = [];

  @override
  void initState() {
    super.initState();

    _loadConditionInfo();
    _loadHistory();
  }

  Future<void> _loadConditionInfo() async {
    final raw = await rootBundle.loadString('assets/skin_conditions.json');
    final Map<String, dynamic> data = json.decode(raw);
    setState(() {
      conditionInfo = data;
      classNames = data.keys.toList();
    });
  }
  Future<void> _loadHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = prefs.getString('scan_history') ?? '[]';
    setState(() {
      _history = ScanRecord.decodeList(jsonStr);
    });
  }

  void _showDiseaseDetails(String className) {
    final info = conditionInfo[className] as Map<String, dynamic>?;

    if (info == null) {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("No info available for $className"))
      );
      return;
    }

    final desc   = info['description'] as String;
    final img    = info['image'] as String;
    final treats = (info['treatments'] as List)
        .cast<Map<String, dynamic>>();

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => Container(
        height: MediaQuery.of(context).size.height * 0.6,
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.red[300],
          borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Align(
              alignment: Alignment.topRight,
              child: IconButton(
                icon: const Icon(Icons.close, color: Colors.white, size: 28),
                onPressed: () => Navigator.pop(context),
              ),
            ),
            Row(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(10),
                  child: Image.asset(img,
                      height: 80, width: 80, fit: BoxFit.cover),
                ),
                const SizedBox(width: 15),
                Expanded(
                  child: Text(className,
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 15),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(desc, textAlign: TextAlign.center),
            ),
            const SizedBox(height: 20),
            const Text("Recommended Treatment:",
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 10),
            for (var t in treats)
              Row(
                children: [
                  Image.asset(t['image'] as String,
                      height: 40, width: 40),
                  const SizedBox(width: 10),
                  Text(t['name'] as String,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[300],
      bottomNavigationBar: const NavBar(currentIndex: 0),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [

              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 25),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Icon(Icons.wb_sunny, size: 45, color: Colors.orange),
                    GestureDetector(
                      onTap: () => Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const Settings()),
                      ),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(10),
                        child: Image.asset(
                          'lib/images/profile.png',
                          width: 70, height: 70, fit: BoxFit.cover,
                          errorBuilder: (_, __, ___) => Container(
                            width: 70, height: 70,
                            decoration: BoxDecoration(
                              color: Colors.grey[300],
                              borderRadius: BorderRadius.circular(25),
                            ),
                            child: const Icon(Icons.person, size: 30),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 10),

              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Welcome Home'),
                    Text('Dhruv Kumar', style: TextStyle(fontSize: 40)),
                  ],
                ),
              ),

              const SizedBox(height: 20),

              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40),
                child: Divider(color: Colors.black, thickness: 2),
              ),

              const SizedBox(height: 20),
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 20),
                padding: const EdgeInsets.all(16),
                width: 400, height: 200,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 6,
                      spreadRadius: 2,
                    ),
                  ],
                ),
                child: _history.isEmpty
                    ? const Center(
                  child: Text(
                    'No scans available',
                    style: TextStyle(
                        fontSize: 18, fontWeight: FontWeight.bold
                    ),
                  ),
                )
                    : Row(
                  children: [
                    ClipRRect(
                      borderRadius: BorderRadius.circular(12),
                      child: Image.file(
                        File(_history.last.imagePath),
                        width: 150, height: 150, fit: BoxFit.cover,
                        errorBuilder: (_, __, ___) =>
                        const Icon(Icons.broken_image, size: 80),
                      ),
                    ),
                    const SizedBox(width: 16),
                    // info
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            _history.last.label,
                            style: const TextStyle(
                                fontSize: 25,
                                fontWeight: FontWeight.bold
                            ),
                          ),
                          const SizedBox(height: 4),
                          Builder(builder: (_) {
                            final rawConf = _history.last.confidence;
                            final displayConf = rawConf > 1 ? rawConf : rawConf * 100;
                            return Text(
                              '${displayConf.toStringAsFixed(1)}%',
                            );
                          }),
                          const SizedBox(height: 4),
                          Text(
                            _history.last.timestamp
                                .toLocal()
                                .toString()
                                .split('.')[0],
                            style: TextStyle(
                                fontSize: 18,
                                color: Colors.grey[600]
                            ),
                          ),
                        ],
                      ),
                    )
                  ],
                ),
              ),

              const SizedBox(height: 20),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: SizedBox(
                  height: 250,
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: classNames.length,
                    itemBuilder: (_, idx) {
                      final name = classNames[idx];
                      final img  = conditionInfo[name]?['image'] as String? ?? '';
                      return GestureDetector(
                        onTap: () => _showDiseaseDetails(name),
                        child: Container(
                          width: 250,
                          margin: const EdgeInsets.only(right: 15),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(15),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.1),
                                blurRadius: 6,
                                spreadRadius: 2,
                              ),
                            ],
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              if (img.isNotEmpty)
                                ClipRRect(
                                  borderRadius: BorderRadius.circular(10),
                                  child: Image.asset(img,
                                      height: 200, width: 200, fit: BoxFit.cover),
                                )
                              else
                                SizedBox(
                                  height: 200,
                                  child: Center(child: Text(name)),
                                ),
                              const SizedBox(height: 10),
                              Text(name,
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16,
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ),

              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}
