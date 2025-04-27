import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/services.dart';
import 'package:image/image.dart' as img;
import 'package:tflite_flutter/tflite_flutter.dart';

class TFLiteService {
  late Interpreter _interpreter;
  late int numClasses;

  late Map<int, String> labels;

  static const int inputSize   = 224;
  static const int numChannels = 3;

  // loads both model + JSON labels so ican debug
  Future<void> loadModel() async {

    _interpreter = await Interpreter.fromAsset('assets/best_model.tflite');
    print(' TFLite loaded');

    // loadin our index and label map
    final rawLabels = await rootBundle.loadString('assets/index_to_label.json');
    final Map<String, dynamic> jsonMap = json.decode(rawLabels);
    labels = jsonMap.map((k, v) => MapEntry(int.parse(k), v as String));
    print(' Loaded ${labels.length} labels');

    // dubgging and testing
    final outTensors = _interpreter.getOutputTensors();

    numClasses = outTensors.first.shape[1];
    print(' model actually returns $numClasses classes');
  }


  Future<List<double>> runInference(Uint8List bytes) async {
    // decode & resize
    final image = img.decodeImage(bytes);
    if (image == null) throw Exception('Cannot decode image bytes');
    final resized = img.copyResize(image,
      width: inputSize,
      height: inputSize,
    );


    final input = Float32List(inputSize * inputSize * numChannels);
    int offset = 0;
    for (var y = 0; y < inputSize; y++) {
      for (var x = 0; x < inputSize; x++) {
        final px = resized.getPixel(x, y);
        input[offset++] = ((px >> 16) & 0xFF) / 255.0;
        input[offset++] = ((px >> 8)  & 0xFF) / 255.0;
        input[offset++] = (px         & 0xFF) / 255.0;
      }
    }

    final output = List.filled(numClasses, 0.0).reshape([1, numClasses]);


    _interpreter.run(
      input.reshape([1, inputSize, inputSize, numChannels]),
      output,
    );

    return List<double>.from(output[0]);
  }
}
