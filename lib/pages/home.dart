import 'package:flutter/material.dart';
import 'package:skinsensor2025/componenets/nav_bar.dart';
import 'package:skinsensor2025/pages/settings.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int skinHealthScore = 0;
  int accuracyScore = 0;
  String detectedCondition = "N/A";

  @override
  void initState() {
    super.initState();
    _loadDiagnosisResults();
  }
  Future<void> _loadDiagnosisResults() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      skinHealthScore = prefs.getInt('skinHealthScore') ?? 0;
      accuracyScore = prefs.getInt('accuracyScore') ?? 0;
      detectedCondition = prefs.getString('detectedCondition') ?? "N/A";
    });


  }


  String _getSkinAdvice(int score) {
    if (score >= 80) {
      return "Wow, your skin is in great condition! Keep using your skincare routine and stay hydrated.";
    } else if (score >= 60) {
      return "Your skin is doing well, but some improvements could help. Consider using a moisturizer daily.";
    } else {
      return "Your skin could use some care. Consider consulting a dermatologist and maintaining hydration.";
    }
  }


  final List<Map<String, dynamic>> skinConditions = [
    {
      "name": "Acne",
      "image": "lib/images/holder.jpg",
      "description": "Acne is caused by clogged pores, leading to pimples, blackheads, and whiteheads.",
      "treatments": [
        {"name": "Benzoyl Peroxide", "image": "lib/images/holder.jpg"},
        {"name": "Salicylic Acid", "image": "lib/images/holder.jpg"},
      ]
    },
    {
      "name": "Eczema",
      "image": "lib/images/holder.jpg",
      "description": "Eczema causes dry, itchy, and inflamed skin, often triggered by allergies or irritants.",
      "treatments": [
        {"name": "Moisturizing Cream", "image": "lib/images/holder.jpg"},
        {"name": "Avoid Hot Showers", "image": "lib/images/holder.jpg"},
      ]
    },
    {
      "name": "Psoriasis",
      "image": "lib/images/holder.jpg",
      "description": "Psoriasis is a chronic autoimmune condition that leads to scaly, red patches on the skin.",
      "treatments": [
        {"name": "Coal Tar Shampoo", "image": "lib/images/holder.jpg"},
        {"name": "Vitamin D Cream", "image": "lib/images/holder.jpg"},
      ]
    },
  ];


  void _showDiseaseDetails(BuildContext context, Map<String, dynamic> condition) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) {
        return Container(
          height: MediaQuery.of(context).size.height * 0.5,
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
                    child: Image.asset(
                      condition["image"]!,
                      height: 80,
                      width: 80,
                      fit: BoxFit.cover,
                    ),
                  ),
                  const SizedBox(width: 15),
                  Expanded(
                    child: Text(
                      condition["name"],
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

              // Description
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  condition["description"],
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontSize: 16),
                ),
              ),
              const SizedBox(height: 20),


              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "Recommended Treatment:",
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 10),
                    for (var treatment in condition["treatments"])
                      Row(
                        children: [
                          Image.asset(treatment["image"]!, height: 40, width: 40),
                          const SizedBox(width: 10),
                          Text(
                            treatment["name"]!,
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
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
              // ✅ App Bar Section
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40.0, vertical: 25),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Icon(Icons.wb_sunny, size: 45, color: Colors.orange), // Sunny Weather



                    GestureDetector(
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const Settings()),
                        );
                      },
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(10),
                        child: Image.asset(
                          'lib/images/profile.png',
                          width: 70,
                          height: 70,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) {
                            return Container(
                              width: 70,
                              height: 70,
                              decoration: BoxDecoration(
                                color: Colors.grey[300],
                                borderRadius: BorderRadius.circular(25),
                              ),
                              child: const Icon(Icons.person, size: 30, color: Colors.black),
                            );
                          },
                        ),
                      ),
                    ),
                  ],
                ),
              ),




              const SizedBox(height: 10),

              // Welcome Text
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Welcome Home'),
                    Text(
                      'Dhruv Kumar',
                      style: TextStyle(fontSize: 40),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 20),

              // Divider
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40.0),
                child: Divider(color: Colors.black, thickness: 2),
              ),

              const SizedBox(height: 20),

              Container(
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
                padding: const EdgeInsets.all(16),
                margin: const EdgeInsets.symmetric(horizontal: 20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [

                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.favorite, color: Colors.red, size: 50),
                        const SizedBox(width: 5),
                        Text(
                          "$skinHealthScore",
                          style: const TextStyle(
                            fontSize: 40,
                            fontWeight: FontWeight.bold,
                            color: Colors.red,
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 5),


                    const Text(
                      'Skin Health Score',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 5),


                    Text(
                      _getSkinAdvice(skinHealthScore),
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 16,
                        color: Colors.black87,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),


              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20.0),
                child: SizedBox(
                  height: 250,
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: skinConditions.length,
                    itemBuilder: (context, index) {
                      final condition = skinConditions[index];
                      return GestureDetector(
                        onTap: () => _showDiseaseDetails(context, condition),
                        child: Container(
                          width: 250,
                          margin: const EdgeInsets.only(right: 15),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(15),
                            boxShadow: [
                              BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 6, spreadRadius: 2),
                            ],
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              ClipRRect(
                                borderRadius: BorderRadius.circular(10),
                                child: Image.asset(condition["image"]!, height: 200, width: 200, fit: BoxFit.cover),
                              ),
                              const SizedBox(height: 10),
                              Text(condition["name"]!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
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
