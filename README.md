# Soft Machine 01


![soft machine zero v42 fll](https://github.com/user-attachments/assets/a66a63b1-a3b4-4041-85fa-c523e927985c)| ![image](https://github.com/user-attachments/assets/018fb950-79fd-474e-acaf-8e5481559526)
--|--|


## Introduction
**S**cientificly **O**ptimized hardware **F**or reducing cost of **T**ransport / **Machine** no.**01**

소프트 머신은 수송비용(COT)을 최소화하기 위해 과학적 사고를 통해 최적화된 오픈소스 키드사이즈 휴머노이드 로봇 플랫폼입니다.

MIT Cheetah로부터 영감을 받아 2024년부터 개인 연구로 진행되고 있으며, 생체역학적 사고와 물리학에 기반하여 최적화된 고성능 하드웨어 기술을 교육용 키드사이즈 로봇에서도 접할 수 있도록 앞당기는 것을 목표로 합니다.

This project is an open-source, kid-sized humanoid robot that minimizes transportation costs (COT) through bio-inspired designs and inertia moment optimization. Dive into the world of robotic innovation, where biomechanics meets advanced robotics engineering.

## Behind Story
소프트 머신의 이름은 1961년 출판된 윌리엄 버로스의 소설, '소프트 머신'으로부터 영감을 받았습니다.

소프트 머신은 새로운 문학적 표현을 위해 '컷업'이라 불리는 글의 단락을 임의로 자르고 재배열하는 실험적인 형식에 기반하여 작성되었습니다.

인간 신체를 프로그래밍이나 해킹이 가능한 일종의 '부드러운 기계'로 접근하며, 용어 소프트 머신은 인간 자체와 인간의 신체를 지칭하는 데 사용됩니다.

본 소프트 머신 프로젝트 또한 인체를 부드러운 기계로 바라보며, 이 기계에 존재하는 에너지 효율 개선 기작들을 실험적인 사고를 통해 실제 기계장치로 구현하고자 합니다.

## Features
**생체역학적 디자인**: 인체의 순간회전중심경로 특성을 구현하여 무게중심의 수직 변화를 최소화하여 에너지 효율적인 스트레치 워크를 가능하게 만듭니다.

**관성 모멘트 최적화**: 액추에이터를 배치하는 단계에서부터 관성 모멘트 최적화를 거쳐 최소한의 역학적 에너지만을 요구하도록 지향하며 설계되었습니다.

**에너지 회수 기작**: 인간의 경우 발을 땅에 딛는 순간 아킬레스건이 신장되며 버려지는 운동 에너지가 용수철 퍼텐셜 에너지로 저장됩니다. 이 에너지는 적절한 시점에 다시 운동에너지로 방출되어 전진을 위한 추진력으로 사용되며 이를 통해 약 60%의 에너지를 절약할 수 있습니다.
소프트 머신 또한 현재 개발 단계에 있는 '머슬 엔진' 하드웨어를 장착하면, 보행 과정에서 버려지는 운동 에너지를 슈퍼 커패시터 충전을 위해 사용합니다. 이 에너지는 적절한 시점에 다시 운동에너지로 방출됩니다.

**오픈소스**: 가능한 모든 부품을 가정용 FDM 3D프린터를 사용하여 제작할 수 있도록 최적화하였으며 모든 하드웨어 설계도와 소프트웨어는 비상업적 사용범위 내에서 무상으로 이용 가능합니다.
기계부를 구성하는 모든 부품에 대한 설계도는 SoftMachine01.F3Z에서 다운로드 받을 수 있으며 전자부의 경우 제 MuscleEngine01 레포지토리에서 작업 진행 현황과 스키메틱 다이어그램을 확인하실 수 있습니다.


## Structure
![soft machine zero v41 dis2](https://github.com/user-attachments/assets/67810a04-e44f-4b01-a092-a57b7b74d16b)| ![soft machine zero v41 dis](https://github.com/user-attachments/assets/892d8998-96c8-4a2e-89a4-0fab040ae9f5)
--|--|

https://a360.co/3A26VUs

소프트 머신은 다음 계층 구조로 제작되었습니다.
Upper Pelvis(보라색) -> Lower Pelvis(파란색) --> Inner Femur(청록색) -> Outer Femur(분홍색) --> Inner Tibia(보라색) -> Outer Tibia(분홍색) --> Achilles(연두색) --> Ankle(노란색)
SoftMachine01.F3Z 파일을 참고하세요.


## Works in Progress
현재 대부분의 기구부 설계가 완료되었지만, 현재 업데이트가 진행 중인 부분들이 있습니다.

### 1. Achilles의 굽힘 문제 해결
주어진 디자인스페이스 내에 Achilles Driver, Achilles, Ankle을 같은 축 상에 배열하는 문제가 해결되지 않았습니다. 현재 이 세 부품이 동일한 선상에 배열되어있지 않아 Achilles가 파괴역학적 관점에서 보(beam)로 작용하고, 이로 인해 불필요한 굽힘력을 받습니다. 이상적인 Achilles는 압축력만을 받는 이상적인 기둥(column)으로 작용해야합니다.

### 2. 회생제동장치 설계
시스템에서 각 관절이 감속할 때, 일반적으로는 버려지는 운동에너지를 전기에너지로 변환하고 슈퍼커패시터에 저장하였다가 시스템이 급가속할 때 이를 꺼내 사용하는 아이디어를 통해 수송비용(COT)을 극단적으로 낮추고자 합니다. 작업 상황은 제 MuscleEngine01 레포지토리에 업데이트되고 있습니다.

### 3. 회생제동 장치와 기구부 디자인의 융합
앞서 언급한 회생제동 시스템을 사용하면 회수된 에너지를 저장하기 위해 큰 용량의 커패시터가 요구됩니다. 키드사이즈 휴머노이드에서 이를 위한 공간을 할당하는 것에는 어려움이 있습니다.

현재 정적응력해석을 통해 응력해소구간을 탐색하고, 이 응력해소구간을 원형으로 타공하여 확보한 공간에 슈퍼커패시터를 장착하는 실험적인 디자인에 대한 연구를 진행하고 있습니다. 이 문서의 최상단에 있는 두 사진을 확인해주세요.
