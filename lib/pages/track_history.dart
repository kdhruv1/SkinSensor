
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:skinsensor2025/componenets/nav_bar.dart';
import 'package:skinsensor2025/componenets/scan_records.dart';

class TrackHistoryPage extends StatefulWidget {
  const TrackHistoryPage({super.key});

  @override
  State<TrackHistoryPage> createState() => _TrackHistoryPageState();
}

class _TrackHistoryPageState extends State<TrackHistoryPage> {
  List<ScanRecord> _history = [];

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = prefs.getString('scan_history') ?? '[]';
    setState(() {
      _history = ScanRecord.decodeList(jsonStr);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[300],
      appBar: AppBar(
        title: const Text('Scan History'),
        backgroundColor: Colors.red[300],
      ),
      body: SafeArea(
        child: _history.isEmpty
            ? const Center(child: Text('No scans yet.'))
            : ListView.builder(
          padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 20),
          itemCount: _history.length,
          itemBuilder: (ctx, i) {
            final rec = _history[i];
            return Container(
              margin: const EdgeInsets.only(bottom: 16),
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
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Timestamp
                    Text(
                      rec.timestamp.toLocal().toString().split('.')[0],
                      style: TextStyle(
                        color: Colors.grey[600],
                        fontSize: 12,
                      ),
                    ),
                    const SizedBox(height: 8),

                    // Scanned Image
                    ClipRRect(
                      borderRadius: BorderRadius.circular(12),
                      child: SizedBox(
                        height: 200,
                        width: double.infinity,
                        child: Image.file(
                          File(rec.imagePath),
                          fit: BoxFit.cover,
                          errorBuilder: (_, __, ___) =>
                          const Center(child: Text('Image not found')),
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Result
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.green[100],
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        '${rec.label} — ${rec.confidence.toStringAsFixed(1)}%',
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
      bottomNavigationBar: const NavBar(currentIndex: 2),
    );
  }
}

