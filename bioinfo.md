## 필요 지식
- 통계(수리통계, 회귀분석, R)
- 컴공(이산수학, 데이터)
- 바이오(분자생물학, 유전학)

## 하는 일
- 도구 : R, Python
- 항암 표적물질 발굴
- 기본 유전체 표준 Reference 제작
- SNP : 단일 염기서열 변화

## 테라젠바이오
- 업계 1위 마크로젠은 공장처럼 돌아가는 분위기?
- 개인 능력 향상과 하고 싶은 일을 하기 위해 선택
- K-DNA 사업 등 국책과제가 제일 많음

PCR ~ NGS
한양대 융합생명공학

생물정보학 _ 인공지능 _ 의생명 데이터사이언스
융합 sw(데이터 사이언스)
혼자 다 배울 수는 없다; 휴먼 네트워크

마크로젠 테라젠 DNA링크
휴앤바이옴(미생물 쪽)

하수처리
원폭피해자
유기견나이(다른 종들의 같은 바이오마커 찾는 과정이 힘들었음)

후성유전체학!

## NGS
- 이전에는 700~1000개 base pair 밖에 읽을 수 없었음
- downstream analysis : 시퀀싱 과정이 편해짐에 따라 중요도 가중
  - 시퀀싱데이터 해석할 수 있을 뿐만 아니라 생물학적 통찰을 찾을 수 있는 사람
- 실제 작용하는 건 RNA, 단백질이나 DNA ~ RNA 서열만 읽을 수 있음
- biological replicate 우선, technical replicate 차선
- fastq : 151bp 염기서열
- normalization은 필수, 연구자들 사이에 합의가 이루어짐
- NGS 데이터 생산은 점점 쉬워지나, 적합한 분석을 할 줄 아는 것은 더 어려워진다
- 

## EDA
> 탐색적 데이터 분석, 데이터를 처음 접하는 사람들이 데이터의 구조와 패턴을 파악하기 위해 사용, 견적을 내는 일
- 획득한 데이터에 대해 critic한 태도를 유지

### EDA의 대상
- 일변량(Univariate)
  - EDA를 통해 한 번에 파악하려는 변수가 1개
  
- 다변량 변수
  - EDA를 통해 한 번에 파악하려는 변수가 여러 개
  - 변수들 간의 관계를 보는 것이 주요 목적

### EDA의 종류
- 시각화(Graphic) : 차트 혹은 그림 등을 이용해 데이터 확인, 데이터를 한 눈에 파악 용이
- 비시각화(Non-Graphic) : 주로 summary statistics 활용, 정확한 데이터값 파악 용이

### EDA의 유형
- 일변량 비시각화(Uni - Non Graphic)
  - 주어진 데이터의 분산(distribution)을 확인하는 것이 주목적
  - 수치형 자료라면 summary statistics를 주로 활용한다.
  - 범주형 자료라면 발생(occurence), 빈도(frequency), 탭화(tabulation)

- 일변량 시각화(Uni - Graphic)
  - 주어진 데이터를 전체적으로 살펴보는 것이 주목적
  - Histogram, pie chart, stem-leaf plot, boxplot, QQplot..
  - 값들이 다양하다면 binning, tabulation 등 활용 가능
  
- 다변량 비시각화(Multi - Non Graphic)
  - 변수간 관계(relationship)를 확인하는 것이 주목적
  - cross-tabulation, cross-statistics(correlation, covariance) 등 활용
  - 범주형 데이터는 행과 열을 바꾸는 cross-tabulation 적용가능
  - 수치형 데이터는 cross statistics 활용가능
  
- 다변량 시각화(Multi - Graphic)
  - 범주형과 수치형은 boxplot, stacked bar, parallel coordinate, heatmap
  - 수치형끼리는 scatter plot 등
  
- Negative control : 분석이 올바르게 수행되었다면 이 값이 반드시 나오지 않음
- Positive control : 분석이 올바르게 수행되었다면 이 값이 반드시 도출됨
- bulk RNA-seq $\rightarrow$ scRNA-seq

## Central Dogma
### DNA
> 생명체의 설계도
- 하나의 세포당 1 copy 존재한다
- 이중나선의 안정적 구조, A, G, C, T 염기서열로 구성
- 복제 중 오류 발생 시 repair 기작이 발달
  - mutation 발생 시 암 발생
- 전체 DNA 중 3~5%만 실제 RNA 및 단백질로 발현된다(=exome)
- DNA 영역을 전체 sequencing 하는 WGRS
- 실제 코딩이 진행되는 영역만을 시퀀싱하는 WES
- 특정 타깃만을 시퀀싱하는 Target sequencing
- cDNA : 한번 전사되었던 RNA를 DNA로 되돌림 (실험 등 목적으로 RNA를 안정적으로 유지하기 위함)
  - coding되지 않은 DNA서열이 존재하지 않음
  - 현대의 sequencer가 ATGC 서열만 해독 가능하기 때문에 활용
  
### RNA
> 단백질의 중간과정으로 여겨졌으나 자체적으로 효소로 작용하는 등 특이기능 연구 중
- A, G, C, U의 염기서열로 구성, 단일가닥으로 존재하여 불안정한 구조
- 단백질로 전환이 되는 mRNA, 염기서열과 일치하는 단백질을 옮기는 tRNA, 리보솜을 구성하는 rRNA 등
- 하나의 DNA 서열로부터 여러개의 RNA transcript가 생겨날 수 있다
  - RNA 성숙과정에서 엑손들의 배치 순서 및 포함여부 결정
- RNA maturation : pre-mRNA에서 인트론 서열이 제거되는 과정
- mRNA는 RNA maturation 완료 후 3' end 쪽에 poly-A tail이 capping 된다(RNA 분해효소 기능 억제)
- transcription factor(TF) 단백질, RNA polymerase 단백질이 전사를 돕는다
  - RNA 연구 시 굉장히 중유하게 고려해야할 요소
- miRNA : dicer protein과 결합하여 스스로와 상보적인 서열을 가지는 RNA 서열을 절단함으로서 발현 조절

### Protein
> 최종적으로 생체 내 현상을 매개하는 분자단계
- 세 개의 RNA 서열로부터 아미노산 서열을 합성(codon)
- mRNA에 리보솜이 결합하여 상보적인 tRNA가 배달하는 아미노산들이 하나의 가닥으로 조립됨

### Insight
- DNA는 특정한 조건이 아닌 이상 일정한 수를 유지하며, 생체 과정을 매개할 때 양이 변화하는 것은 RNA, Protein
- RNA나 Protein의 발현량이 변화했다
- 분자 단계의 발현량 변화가 최종적으로 어떠한 표현형(눈에 보이는 형질)의 변화로 이어진다

## RNA-seq
### 순서
- 시퀀싱
  
- raw reads(fastq)
  - 시퀀싱으로 읽은 서열정보 raw data
  - 151bp를 하나의 reads로 하여 6M ~ 10M개 정도의 reads 수를 확보해야
  
- Alignment
  - 참조 서열에 mapping 하는 작업
  - 참조서열 정보가 없는 경우 DNA-seq을 통해 참조서열 구축
  
- Quantification
  - gene_expression.xlsx파일 등 ; Quantification 완료된 상태
  - align을 마치고 mapping된 reads를 count
  - 특정 유전자 영역에 매핑된 reads의 수를 의미하며, 유전자의 발현값으로 분석하기 위해서는 반드시 생산량을 고려하여 정규화(normalization) 과정이 필요

- Down-stream analysis

### 부가설명
- Tuxedo Protocol
  > 전반적인 워크플로우에 사용되는 툴 들의 이름이 턱시도와 관련된 이름들이라서

- Normalization
  - R/FPKM
  - TPM
  - TMM

- 약점 : RNA가 많이 발현된다고 반드시 Protein이 많이 발현되는 것은 아니다

DEG분석
  edgeR

  input을 specific하게 지정하기
  bioinfo 파이프 라인 >> 사용되는 툴 사이의 인풋과 아웃풋을 맞추는 것이 절반?
  차등발현 유전자가 어떠한 pathway(기능, 표현형?)와 연관이 있는가

### pathway 분석론
- 1세대 pathway 분석 방법론
  - GSEA, DAVID
  - ORA : 직관적으로 p-value높은 것이 연관성이 있다고 판단
- 2세대 pathway 분석 방법론
  - 내가 뽑은 차등발현유전자가 아슬아슬하게 발현시키는 경우 p-value가 크게 나오나 실제 연관되는 것보다 과장되어 pathway와 연관되어 있다고 결론지어질 가능성이 있는데, 2세대는 발현량을 같이 고려해서 pathway와 연관시키기 때문에 상대적으로 데이터의 왜곡이 발생할 가능성을 낮추는 방법이다.
  - GSEA, 널리 사용되어 2세대 방법론을 GSEA라고 칭하는 경우도
  - 한 눈에 봤을 때 직관성은 떨어지나 읽는 방법만 알아 놓으면 해석하기 편한 방법이다.
  - 데이터 포매팅이 약간 필요해서 손이 들어가긴 하나 그에 비해 얻을 수 있는 것이 많아 universial하게 사용됨
- 3세대 pathway
  - 단점 : 데이터 포매팅이 어렵고 리소스를 많이 차지한다. 추가적으로 정의해야 할 요소들이 많다
  - 장점 : 메타데이터(분석조건)을 굉장히 다원화 시킬 수 있다. 여러가지 변량 간의 연관도 등
  - 네트워크 애널리시스 : pathway 사이에 network를 연결해준다. 온갖 방법론에 따른 툴들이 즐비함.

- 세대로 구분하나, 차 세대가 이전세대를 완벽히 커버하는 것은 아님

분자생물학과 전반적인 워크플로우
BI, 하이브리드 직종으로 컴퓨터사이언스, 생물학적 인사이트 중 어느곳에 중점을 두어야 하는가
Technician vs Scientist, 당연히 생물학적 인사이트에 중점을 두어야 한다
컴퓨터사이언스는 보조할 수 있는 수단들이 많다.

## 분석 논문
- 논리전개 방식을 알아두기
- 논문 리뷰

## GEO 활용 RNA-Seq
- 같은 샘플을 가지고 실험했기 때문에 결과가 크게 다르면 안 됨
- EDA과정 : histogram, scatter plot, box plot을 확인해 데이터간의 전반적인 분포확인
- DEG분석 : edgeR

## GSEA
> 2세대 pathway analysis

### 과정
- Gene expression data(.gct)
- phenotype data(.cls)
- DB 파일을 다운로드 받아왔을 때도 구조 확인하는 버릇
- Gene Set Database(.gmt)
- Ranked Gene Lists(.rnk)

### 단점
- data prep과정이 번거롭다
- 데이터를 분석하는데에 있어 비직관적이다
- 스크립트를 통한 자동화 불가능

## fGESA
> fast Gene Set Enrichment Analysis
- GSEA 방법론 자체는 우수하나 프로그램의 단점이 많음
- bioconductor tool중 40번째로 많이 사용됨

어느 유전자나 단백질이 어떤 상황에서 많이 발현되느냐?

## DB
### GEO

### TCGA
- GDC를 통해
- GEO보다 양질의 데이터
- 암정복에 대한 단서는 이미 TCGA에 올라와 있을 것이다

## 새로운 방법론
- RNA-Seq based
  
### scRNA-Seq
- 암에 걸렸다고 가정하면 어느 세포는 정상세포이고, 어느 세포는 암세포일 것인데 기존 mRNA-Seq은 전체 세포를 하나의 데이터로 만들어 분석하나, single cell RNA-Seq은 세포 하나별 데이터를 보존하여 섬세한 결과를 도출 가능
- RNA Seq보다 비직관적

### Spatial transcriptomics
> 세포의 실제 위치에 따라 발현되는 유전자의 차이를 구분

### Multiomic Analysis    
> genomics(DNA) + transcriptomics(RNA) + proteomics(Protein)

## Cloud Computing
|on-premises|cloud computing|
|--|--|
|높은 초기 투자 비용|사용한 만큼만 지불|
|한정된 용량|유연한 용량|
|많은 공수 및 소요시간|적은 노력 및 소요시간|