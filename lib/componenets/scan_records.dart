import 'dart:convert';

class ScanRecord {
  final String imagePath;
  final String label;
  final double confidence;
  final DateTime timestamp;

  ScanRecord({
    required this.imagePath,
    required this.label,
    required this.confidence,
    required this.timestamp,
  });

  Map<String, dynamic> toJson() => {
    'imagePath': imagePath,
    'label': label,
    'confidence': confidence,
    'timestamp': timestamp.toIso8601String(),
  };

  factory ScanRecord.fromJson(Map<String, dynamic> m) => ScanRecord(
    imagePath: m['imagePath'] as String,
    label: m['label'] as String,
    confidence: (m['confidence'] as num).toDouble(),
    timestamp: DateTime.parse(m['timestamp'] as String),
  );

  static String encodeList(List<ScanRecord> records) =>
      json.encode(records.map((r) => r.toJson()).toList());

  static List<ScanRecord> decodeList(String jsonStr) {
    final List decoded = json.decode(jsonStr) as List;
    return decoded
        .map((e) => ScanRecord.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
