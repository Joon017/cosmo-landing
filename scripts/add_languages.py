"""Create 8 new localized pages and update hreflang + lang switcher across all pages."""

import re, os, shutil

base = 'c:/Users/joony/OneDrive/Desktop/cosmo-landing'

# ── Translations ────────────────────────────────────────────────────────────

translations = {
    'ja': {
        'html_lang': 'ja',
        'hero_sub': 'Cosmoはリアルな会話のために設計されており、70以上の言語でリアルタイムに双方向の会話を正確かつ確実に翻訳します。言語の壁を取り除き、無限の可能性を解き放つお手伝いをします。',
        'store_label': 'iOS・Androidで無料試用',
        'stat_languages': '70以上の対応言語',
        'stat_credits': '無料クレジット20個でスタート',
        'uc_eyebrow': '使用例',
        'uc_title': 'あらゆる会話のために設計',
        'uc_sub': '国境を越えても、ビジネスでも、Cosmoがあなたの言葉を伝えます。',
        'uc_tag_1': '旅行',
        'uc_h3_1': '旅行と日常会話',
        'uc_p_1': '自信を持って新しい場所を探索しましょう。道を尋ねたり、食事を注文したり、地元の人と交流したり。会話帳は不要です。Cosmoが会話を処理するので、あなたは体験に集中できます。',
        'uc_tag_2': 'ホスピタリティ',
        'uc_h3_2': 'ホテルとゲストサービス',
        'uc_p_2': 'チェックインからコンシェルジュのリクエストまで、Cosmoは異なる言語を話すスタッフとゲストの橋渡しをし、すべての滞在をスムーズでパーソナルなものにします。',
        'uc_tag_3': 'ビジネス',
        'uc_h3_3': 'ビジネス会議と交渉',
        'uc_p_3': 'どんな会議室にも準備万端で入れます。Cosmoが双方向でライブ翻訳し、世界中のパートナーとリアルタイムで交渉、協力、関係構築ができます。',
        'lang_eyebrow': '対応言語',
        'lang_title': 'どこでも誰とでも話せる',
        'lang_sub': 'Cosmoは70以上の言語に対応しています。広く話されている言語から地域言語まで。利用可能な言語のサンプル：',
        'lang_more': '…その他多数。完全なリストはアプリ内でご確認ください。',
        'faq_credits_q': '翻訳にクレジットが必要なのはなぜですか？',
        'faq_credits_a': 'Cosmoは高度なAIモデルを使用して、リアルタイムで高速かつ正確で自然な翻訳を提供します。基本的な翻訳アプリとは異なり、すべての会話はコンピューティングパワーを必要とするこれらのモデルを通じて処理されており、それにはコストがかかります。クレジットは、実際に使用した分だけお支払いいただきながら、サービスを維持する方法です。アカウント不要で、20ゲストクレジットから無料で始められます。',
    },
    'ko': {
        'html_lang': 'ko',
        'hero_sub': 'Cosmo는 실제 대화를 위해 설계되었으며, 70개 이상의 언어로 실시간 양방향 대화를 정확하고 신뢰할 수 있게 번역합니다. 언어 장벽을 허물어 무한한 기회를 열어드립니다.',
        'store_label': 'iOS 및 Android에서 무료 체험',
        'stat_languages': '70개 이상 언어 지원',
        'stat_credits': '시작을 위한 20개 무료 크레딧',
        'uc_eyebrow': '사용 사례',
        'uc_title': '모든 대화를 위해 설계',
        'uc_sub': '국경을 넘거나 거래를 성사시킬 때, Cosmo가 당신을 이해시켜 드립니다.',
        'uc_tag_1': '여행',
        'uc_h3_1': '여행 및 일상 대화',
        'uc_p_1': '자신감 있게 새로운 곳을 탐험하세요. 길을 묻고, 음식을 주문하고, 현지인과 교류하세요. 회화책 필요 없습니다. Cosmo가 대화를 처리하니 경험에 집중하세요.',
        'uc_tag_2': '호스피탈리티',
        'uc_h3_2': '호텔 및 고객 서비스',
        'uc_p_2': '체크인부터 컨시어지 요청까지, Cosmo는 다른 언어를 사용하는 직원과 투숙객 사이의 간극을 메워 모든 숙박을 원활하고 개인적으로 만듭니다.',
        'uc_tag_3': '비즈니스',
        'uc_h3_3': '비즈니스 미팅 및 협상',
        'uc_p_3': '어떤 회의실에도 준비된 상태로 입장하세요. Cosmo가 양방향으로 실시간 번역하여 전 세계 파트너와 협상하고 협력하며 관계를 구축할 수 있습니다.',
        'lang_eyebrow': '언어',
        'lang_title': '어디서나 누구와도 대화하세요',
        'lang_sub': 'Cosmo는 70개 이상의 언어를 지원합니다. 널리 사용되는 언어부터 지역 언어까지. 사용 가능한 언어 샘플:',
        'lang_more': '…그 외 더 많은 언어. 전체 목록은 앱에서 확인하세요.',
        'faq_credits_q': '번역에 크레딧이 필요한 이유는 무엇인가요?',
        'faq_credits_a': 'Cosmo는 고급 AI 모델을 사용하여 실시간으로 빠르고 정확하며 자연스러운 번역을 제공합니다. 기본 번역 앱과 달리 모든 대화는 컴퓨팅 파워가 필요한 이 모델들을 통해 처리되며, 비용이 발생합니다. 크레딧은 실제로 사용한 것에만 비용을 지불하면서 서비스를 유지하는 방법입니다. 계정 없이 20개의 게스트 크레딧으로 무료로 시작할 수 있습니다.',
    },
    'pt': {
        'html_lang': 'pt-BR',
        'hero_sub': 'Desenvolvido para conversas reais, o Cosmo traduz conversas bidirecionais ao vivo com precisão e confiabilidade em mais de 70 idiomas em tempo real, para que você e a pessoa à sua frente sempre se entendam. Acreditamos em ajudá-lo a desbloquear oportunidades ilimitadas quebrando a barreira do idioma.',
        'store_label': 'Experimente grátis no iOS e Android',
        'stat_languages': 'Mais de 70 idiomas suportados',
        'stat_credits': '20 créditos grátis para começar',
        'uc_eyebrow': 'Casos de Uso',
        'uc_title': 'Desenvolvido para cada conversa',
        'uc_sub': 'Seja cruzando fronteiras ou fechando negócios, o Cosmo faz você ser entendido.',
        'uc_tag_1': 'Viagem',
        'uc_h3_1': 'Viagens e Conversas do Dia a Dia',
        'uc_p_1': 'Navegue por novos lugares com confiança. Peça direções, faça pedidos e conecte-se com locais. Sem necessidade de guia de conversação. O Cosmo cuida da conversa para que você possa focar na experiência.',
        'uc_tag_2': 'Hospitalidade',
        'uc_h3_2': 'Hotéis e Serviços ao Hóspede',
        'uc_p_2': 'Do check-in às solicitações de concierge, o Cosmo conecta funcionários e hóspedes que falam idiomas diferentes, tornando cada estadia impecável e pessoal.',
        'uc_tag_3': 'Negócios',
        'uc_h3_3': 'Reuniões de Negócios e Negociações',
        'uc_p_3': 'Entre em qualquer sala preparado. O Cosmo traduz ao vivo em ambas as direções para que você possa negociar, colaborar e construir relacionamentos com parceiros do mundo todo, em tempo real.',
        'lang_eyebrow': 'Idiomas',
        'lang_title': 'Fale com qualquer pessoa, em qualquer lugar',
        'lang_sub': "O Cosmo suporta mais de 70 idiomas — dos mais falados aos regionais. Uma amostra do que está disponível:",
        'lang_more': '…e muito mais. Lista completa disponível no aplicativo.',
        'faq_credits_q': 'Por que preciso de créditos para traduzir?',
        'faq_credits_a': 'O Cosmo usa modelos avançados de IA para fornecer traduções rápidas, precisas e naturais em tempo real. Ao contrário de aplicativos de tradução básicos, cada conversa é processada por esses modelos que exigem poder computacional, e isso tem um custo. Os créditos são a forma como mantemos o serviço funcionando enquanto garantimos que você pague apenas pelo que realmente usa. Você pode começar de graça com 20 créditos de convidado, sem necessidade de conta.',
    },
    'de': {
        'html_lang': 'de',
        'hero_sub': 'Für echte Gespräche entwickelt, übersetzt Cosmo bidirektionale Live-Gespräche in über 70 Sprachen präzise und zuverlässig in Echtzeit, damit Sie und Ihr Gesprächspartner sich immer verstehen. Wir helfen Ihnen, unbegrenzte Möglichkeiten zu erschließen, indem wir die Sprachbarriere durchbrechen.',
        'store_label': 'Kostenlos auf iOS und Android testen',
        'stat_languages': '70+ unterstützte Sprachen',
        'stat_credits': '20 Gratis-Credits zum Starten',
        'uc_eyebrow': 'Anwendungsfälle',
        'uc_title': 'Für jedes Gespräch entwickelt',
        'uc_sub': 'Ob Sie Grenzen überschreiten oder Geschäfte abschließen, Cosmo sorgt dafür, dass Sie verstanden werden.',
        'uc_tag_1': 'Reisen',
        'uc_h3_1': 'Reisen und Alltagsgespräche',
        'uc_p_1': 'Erkunden Sie neue Orte mit Zuversicht. Fragen Sie nach dem Weg, bestellen Sie Essen und vernetzen Sie sich mit Einheimischen. Kein Sprachführer nötig. Cosmo übernimmt das Gespräch, damit Sie sich auf das Erlebnis konzentrieren können.',
        'uc_tag_2': 'Gastgewerbe',
        'uc_h3_2': 'Hotels und Gästeservice',
        'uc_p_2': 'Vom Check-in bis zu Concierge-Anfragen überbrückt Cosmo die Kommunikationslücke zwischen Personal und Gästen, die verschiedene Sprachen sprechen, und macht jeden Aufenthalt reibungslos und persönlich.',
        'uc_tag_3': 'Business',
        'uc_h3_3': 'Geschäftsmeetings und Verhandlungen',
        'uc_p_3': 'Betreten Sie jeden Raum gut vorbereitet. Cosmo übersetzt live in beide Richtungen, damit Sie mit Partnern aus aller Welt in Echtzeit verhandeln, zusammenarbeiten und Beziehungen aufbauen können.',
        'lang_eyebrow': 'Sprachen',
        'lang_title': 'Sprechen Sie mit jedem, überall',
        'lang_sub': 'Cosmo unterstützt 70+ Sprachen – von weit verbreiteten bis hin zu regionalen. Eine Auswahl des Verfügbaren:',
        'lang_more': '…und viele mehr. Vollständige Liste in der App verfügbar.',
        'faq_credits_q': 'Warum benötige ich Credits zum Übersetzen?',
        'faq_credits_a': 'Cosmo verwendet fortschrittliche KI-Modelle, um schnelle, präzise und natürlich klingende Übersetzungen in Echtzeit zu liefern. Im Gegensatz zu einfachen Übersetzungs-Apps wird jedes Gespräch durch diese Modelle verarbeitet, die Rechenleistung benötigen, und das hat einen Preis. Credits sind unsere Methode, den Service am Laufen zu halten und gleichzeitig sicherzustellen, dass Sie nur für das bezahlen, was Sie tatsächlich nutzen. Sie können kostenlos mit 20 Gast-Credits starten, ohne Konto erforderlich.',
    },
    'ar': {
        'html_lang': 'ar',
        'rtl': True,
        'hero_sub': 'صُمِّم كوسمو للمحادثات الحقيقية، إذ يترجم المحادثات الثنائية الاتجاه في الوقت الفعلي بدقة وموثوقية لأكثر من 70 لغة، حتى تتفاهم أنت والشخص أمامك دائماً. نؤمن بمساعدتك على فتح آفاق لا محدودة من خلال كسر الحاجز اللغوي.',
        'store_label': 'جرّبه مجاناً على iOS وAndroid',
        'stat_languages': 'يدعم أكثر من 70 لغة',
        'stat_credits': '20 رصيداً مجانياً للبدء',
        'uc_eyebrow': 'حالات الاستخدام',
        'uc_title': 'مصمم لكل محادثة',
        'uc_sub': 'سواء كنت تعبر الحدود أو تُبرم الصفقات، يجعلك كوسمو مفهوماً دائماً.',
        'uc_tag_1': 'السفر',
        'uc_h3_1': 'السفر والمحادثات اليومية',
        'uc_p_1': 'استكشف أماكن جديدة بثقة. اسأل عن الاتجاهات، واطلب الطعام، وتواصل مع السكان المحليين. لا حاجة لكتيب العبارات. يتولى كوسمو المحادثة حتى تتفرغ للتجربة.',
        'uc_tag_2': 'الضيافة',
        'uc_h3_2': 'الفنادق وخدمات الضيوف',
        'uc_p_2': 'من تسجيل الوصول إلى طلبات الكونسيرج، يسد كوسمو الفجوة بين الموظفين والضيوف الناطقين بلغات مختلفة، مما يجعل كل إقامة سلسة وشخصية.',
        'uc_tag_3': 'الأعمال',
        'uc_h3_3': 'اجتماعات الأعمال والمفاوضات',
        'uc_p_3': 'ادخل أي غرفة وأنت مستعد. يترجم كوسمو مباشرةً في الاتجاهين حتى تتمكن من التفاوض والتعاون وبناء العلاقات مع شركاء حول العالم في الوقت الفعلي.',
        'lang_eyebrow': 'اللغات',
        'lang_title': 'تحدث مع أي شخص، في أي مكان',
        'lang_sub': 'يدعم كوسمو أكثر من 70 لغة، من الأكثر انتشاراً إلى الإقليمية. إليك عينة مما هو متاح:',
        'lang_more': '…والمزيد. القائمة الكاملة متاحة في التطبيق.',
        'faq_credits_q': 'لماذا أحتاج إلى أرصدة للترجمة؟',
        'faq_credits_a': 'يستخدم كوسمو نماذج ذكاء اصطناعي متقدمة لتقديم ترجمات سريعة ودقيقة وطبيعية في الوقت الفعلي. على خلاف تطبيقات الترجمة الأساسية، تتم معالجة كل محادثة عبر هذه النماذج التي تتطلب قدرة حوسبية، وهذا له تكلفة. الأرصدة هي طريقتنا للحفاظ على تشغيل الخدمة مع ضمان أنك تدفع فقط مقابل ما تستخدمه فعلاً. يمكنك البدء مجاناً بـ 20 رصيداً للضيوف دون الحاجة إلى حساب.',
    },
    'hi': {
        'html_lang': 'hi',
        'hero_sub': 'वास्तविक बातचीत के लिए बनाया गया, Cosmo 70 से अधिक भाषाओं में रियल-टाइम में दोतरफा बातचीत को सटीक और विश्वसनीय रूप से अनुवाद करता है, ताकि आप और आपके सामने वाला व्यक्ति हमेशा एक-दूसरे को समझ सकें। हम भाषा की बाधा तोड़कर आपके लिए असीमित अवसर खोलने में विश्वास करते हैं।',
        'store_label': 'iOS और Android पर मुफ्त में आज़माएं',
        'stat_languages': '70+ भाषाएं समर्थित',
        'stat_credits': 'शुरू करने के लिए 20 मुफ्त क्रेडिट',
        'uc_eyebrow': 'उपयोग के मामले',
        'uc_title': 'हर बातचीत के लिए बनाया गया',
        'uc_sub': 'चाहे आप सीमाएं पार कर रहे हों या सौदे कर रहे हों, Cosmo आपको समझाता रहता है।',
        'uc_tag_1': 'यात्रा',
        'uc_h3_1': 'यात्रा और दैनिक बातचीत',
        'uc_p_1': 'आत्मविश्वास से नई जगहों की खोज करें। दिशाएं पूछें, खाना ऑर्डर करें और स्थानीय लोगों से जुड़ें। कोई फ्रेज़बुक की जरूरत नहीं। Cosmo बातचीत संभालता है ताकि आप अनुभव पर ध्यान केंद्रित कर सकें।',
        'uc_tag_2': 'आतिथ्य',
        'uc_h3_2': 'होटल और अतिथि सेवाएं',
        'uc_p_2': 'चेक-इन से लेकर कंसिएर्ज अनुरोधों तक, Cosmo विभिन्न भाषाएं बोलने वाले कर्मचारियों और मेहमानों के बीच की खाई को पाटता है, जिससे हर प्रवास निर्बाध और व्यक्तिगत लगता है।',
        'uc_tag_3': 'व्यापार',
        'uc_h3_3': 'व्यापारिक बैठकें और वार्ताएं',
        'uc_p_3': 'किसी भी कमरे में तैयार होकर प्रवेश करें। Cosmo दोनों दिशाओं में लाइव अनुवाद करता है ताकि आप दुनिया भर के भागीदारों के साथ वास्तविक समय में बातचीत कर, सहयोग कर और संबंध बना सकें।',
        'lang_eyebrow': 'भाषाएं',
        'lang_title': 'कहीं भी, किसी से भी बात करें',
        'lang_sub': 'Cosmo 70 से अधिक भाषाओं को सपोर्ट करता है — व्यापक रूप से बोली जाने वाली से लेकर क्षेत्रीय तक। उपलब्ध भाषाओं का एक नमूना:',
        'lang_more': '…और भी बहुत कुछ। पूरी सूची ऐप में उपलब्ध है।',
        'faq_credits_q': 'अनुवाद के लिए क्रेडिट की आवश्यकता क्यों है?',
        'faq_credits_a': 'Cosmo रियल-टाइम में तेज़, सटीक और प्राकृतिक अनुवाद प्रदान करने के लिए उन्नत AI मॉडल का उपयोग करता है। बुनियादी अनुवाद ऐप्स के विपरीत, हर बातचीत इन मॉडलों के माध्यम से संसाधित होती है जिन्हें कम्प्यूटिंग शक्ति की आवश्यकता होती है, और इसकी एक लागत है। क्रेडिट हमारी वह विधि है जिससे हम सेवा चालू रखते हैं और यह सुनिश्चित करते हैं कि आप केवल उतना ही भुगतान करें जितना आप वास्तव में उपयोग करते हैं। आप बिना खाते के 20 गेस्ट क्रेडिट के साथ मुफ्त में शुरू कर सकते हैं।',
    },
    'tr': {
        'html_lang': 'tr',
        'hero_sub': "Gerçek konuşmalar için tasarlanan Cosmo, 70'ten fazla dilde iki yönlü canlı konuşmaları gerçek zamanlı olarak doğru ve güvenilir şekilde çeviriyor; böylece siz ve karşınızdaki kişi her zaman birbirinizi anlıyorsunuz. Dil engelini kırarak sınırsız fırsatların kilidini açmanıza yardımcı olmaya inanıyoruz.",
        'store_label': "iOS ve Android'de ücretsiz deneyin",
        'stat_languages': "70'ten fazla desteklenen dil",
        'stat_credits': 'Başlamak için 20 ücretsiz kredi',
        'uc_eyebrow': 'Kullanım Alanları',
        'uc_title': 'Her konuşma için tasarlandı',
        'uc_sub': 'İster sınırları aşıyor ister anlaşmalar yapıyor olun, Cosmo sizi anlaşılır kılar.',
        'uc_tag_1': 'Seyahat',
        'uc_h3_1': 'Seyahat ve Günlük Konuşmalar',
        'uc_p_1': 'Yeni yerleri güvenle keşfedin. Yol tarifi isteyin, yemek sipariş edin ve yerel halkla bağlantı kurun. Konuşma rehberi gerekmez. Cosmo konuşmayı yönetir, siz deneyime odaklanırsınız.',
        'uc_tag_2': 'Konaklama',
        'uc_h3_2': 'Oteller ve Misafir Hizmetleri',
        'uc_p_2': "Check-in'den konsiyerj taleplerine kadar, Cosmo farklı diller konuşan personel ve misafirler arasındaki uçurumu kapatarak her konaklamayı sorunsuz ve kişisel hale getirir.",
        'uc_tag_3': 'İş',
        'uc_h3_3': 'İş Toplantıları ve Müzakereler',
        'uc_p_3': 'Her odaya hazır girin. Cosmo her iki yönde de canlı çeviri yaparak dünya genelindeki ortaklarla gerçek zamanlı olarak müzakere etmenizi, iş birliği yapmanızı ve ilişkiler kurmanızı sağlar.',
        'lang_eyebrow': 'Diller',
        'lang_title': 'Herkesle, her yerde konuşun',
        'lang_sub': "Cosmo, yaygın konuşulanlardan bölgesel dillere kadar 70'ten fazla dili destekler. Mevcut dillerden bir örnek:",
        'lang_more': '…ve çok daha fazlası. Tam liste uygulamada mevcuttur.',
        'faq_credits_q': 'Çeviri için neden krediye ihtiyaç var?',
        'faq_credits_a': 'Cosmo, gerçek zamanlı olarak hızlı, doğru ve doğal çeviriler sunmak için gelişmiş yapay zeka modelleri kullanır. Temel çeviri uygulamalarının aksine, her konuşma hesaplama gücü gerektiren bu modeller aracılığıyla işlenir ve bunun bir maliyeti vardır. Krediler, yalnızca gerçekten kullandığınız kadar ödeme yapmanızı sağlarken hizmeti sürdürmemizin yoludur. Hesap gerekmeksizin 20 misafir kredisiyle ücretsiz başlayabilirsiniz.',
    },
    'ru': {
        'html_lang': 'ru',
        'hero_sub': 'Разработанный для реальных разговоров, Cosmo точно и надёжно переводит двустороннее живое общение на более чем 70 языках в режиме реального времени, чтобы вы и ваш собеседник всегда понимали друг друга. Мы помогаем вам открывать безграничные возможности, преодолевая языковой барьер.',
        'store_label': 'Попробуйте бесплатно на iOS и Android',
        'stat_languages': 'Поддержка 70+ языков',
        'stat_credits': '20 бесплатных кредитов для начала',
        'uc_eyebrow': 'Сценарии использования',
        'uc_title': 'Создан для каждого разговора',
        'uc_sub': 'Пересекаете ли вы границы или заключаете сделки, Cosmo обеспечит вам взаимопонимание.',
        'uc_tag_1': 'Путешествия',
        'uc_h3_1': 'Путешествия и повседневные разговоры',
        'uc_p_1': 'Исследуйте новые места с уверенностью. Спрашивайте дорогу, заказывайте еду и общайтесь с местными жителями. Разговорник не нужен. Cosmo берёт на себя разговор, чтобы вы могли сосредоточиться на впечатлениях.',
        'uc_tag_2': 'Гостеприимство',
        'uc_h3_2': 'Отели и обслуживание гостей',
        'uc_p_2': 'От заселения до консьерж-услуг, Cosmo устраняет языковой барьер между персоналом и гостями, говорящими на разных языках, делая каждое пребывание комфортным и персональным.',
        'uc_tag_3': 'Бизнес',
        'uc_h3_3': 'Деловые встречи и переговоры',
        'uc_p_3': 'Входите в любую комнату подготовленными. Cosmo переводит в режиме реального времени в обоих направлениях, чтобы вы могли вести переговоры, сотрудничать и строить отношения с партнёрами по всему миру.',
        'lang_eyebrow': 'Языки',
        'lang_title': 'Говорите с кем угодно, где угодно',
        'lang_sub': 'Cosmo поддерживает более 70 языков — от широко распространённых до региональных. Образец доступных языков:',
        'lang_more': '…и многое другое. Полный список доступен в приложении.',
        'faq_credits_q': 'Зачем нужны кредиты для перевода?',
        'faq_credits_a': 'Cosmo использует передовые модели ИИ для обеспечения быстрых, точных и естественно звучащих переводов в реальном времени. В отличие от базовых приложений для перевода, каждый разговор обрабатывается этими моделями, которые требуют вычислительной мощности, и это имеет свою стоимость. Кредиты — это способ поддерживать работу сервиса, гарантируя, что вы платите только за то, что действительно используете. Вы можете начать бесплатно с 20 гостевыми кредитами без необходимости создавать аккаунт.',
    },
}

# ── Language switcher options (all pages) ────────────────────────────────────

NEW_SWITCHER = '''      <select onchange="if(this.value) { localStorage.setItem('cosmo-lang', this.value); window.location = this.value; }">
        <option value="/">EN</option>
        <option value="/es/">ES</option>
        <option value="/fr/">FR</option>
        <option value="/zh/">中文</option>
        <option value="/ja/">日本語</option>
        <option value="/ko/">한국어</option>
        <option value="/pt/">PT</option>
        <option value="/de/">DE</option>
        <option value="/ar/">AR</option>
        <option value="/hi/">HI</option>
        <option value="/tr/">TR</option>
        <option value="/ru/">RU</option>
      </select>'''

# ── hreflang block (goes in <head>) ──────────────────────────────────────────

NEW_HREFLANG = '''  <link rel="alternate" hreflang="en" href="https://getcosmoapp.com/" />
  <link rel="alternate" hreflang="es" href="https://getcosmoapp.com/es/" />
  <link rel="alternate" hreflang="fr" href="https://getcosmoapp.com/fr/" />
  <link rel="alternate" hreflang="zh" href="https://getcosmoapp.com/zh/" />
  <link rel="alternate" hreflang="ja" href="https://getcosmoapp.com/ja/" />
  <link rel="alternate" hreflang="ko" href="https://getcosmoapp.com/ko/" />
  <link rel="alternate" hreflang="pt-BR" href="https://getcosmoapp.com/pt/" />
  <link rel="alternate" hreflang="de" href="https://getcosmoapp.com/de/" />
  <link rel="alternate" hreflang="ar" href="https://getcosmoapp.com/ar/" />
  <link rel="alternate" hreflang="hi" href="https://getcosmoapp.com/hi/" />
  <link rel="alternate" hreflang="tr" href="https://getcosmoapp.com/tr/" />
  <link rel="alternate" hreflang="ru" href="https://getcosmoapp.com/ru/" />
  <link rel="alternate" hreflang="x-default" href="https://getcosmoapp.com/" />'''

# ── Helpers ──────────────────────────────────────────────────────────────────

def update_hreflang(content):
    return re.sub(
        r'<link rel="alternate" hreflang="en".*?<link rel="alternate" hreflang="x-default".*?/>',
        NEW_HREFLANG,
        content,
        flags=re.DOTALL
    )

def update_switcher(content, current_lang_value):
    switcher = NEW_SWITCHER.replace(
        f'<option value="{current_lang_value}">',
        f'<option value="{current_lang_value}" selected>'
    )
    return re.sub(
        r'<select onchange=.*?</select>',
        switcher,
        content,
        flags=re.DOTALL
    )

def apply_translation(content, t):
    content = re.sub(r'<p class="hero-sub">.*?</p>', f'<p class="hero-sub">{t["hero_sub"]}</p>', content, flags=re.DOTALL)
    content = content.replace('Try for free on iOS and Android', t['store_label'])
    content = content.replace('70+ Languages Supported', t['stat_languages'])
    content = content.replace('20 free credits to begin', t['stat_credits'])
    content = content.replace('<div class="eyebrow">Use Cases</div>', f'<div class="eyebrow">{t["uc_eyebrow"]}</div>', 1)
    content = content.replace('<h2 class="section-title">Built for every conversation</h2>', f'<h2 class="section-title">{t["uc_title"]}</h2>', 1)
    content = content.replace("Whether you're crossing borders or closing deals, Cosmo keeps you understood.", t['uc_sub'])
    content = content.replace('<span class="usecase-tag">Travel</span>', f'<span class="usecase-tag">{t["uc_tag_1"]}</span>')
    content = content.replace('<h3>Travel &amp; Daily Conversations</h3>', f'<h3>{t["uc_h3_1"]}</h3>')
    content = content.replace('Navigate new places with confidence. Ask for directions, order food, and connect with locals. No phrasebook needed. Cosmo handles the conversation so you can focus on the experience.', t['uc_p_1'])
    content = content.replace('<span class="usecase-tag">Hospitality</span>', f'<span class="usecase-tag">{t["uc_tag_2"]}</span>')
    content = content.replace('<h3>Hotels &amp; Guest Services</h3>', f'<h3>{t["uc_h3_2"]}</h3>')
    content = content.replace('From check-in to concierge requests, Cosmo bridges the gap between staff and guests speaking different languages, making every stay feel seamless and personal.', t['uc_p_2'])
    content = content.replace('<span class="usecase-tag">Business</span>', f'<span class="usecase-tag">{t["uc_tag_3"]}</span>')
    content = content.replace('<h3>Business Meetings &amp; Negotiations</h3>', f'<h3>{t["uc_h3_3"]}</h3>')
    content = content.replace('Walk into any room ready. Cosmo translates live in both directions so you can negotiate, collaborate, and build relationships with partners around the world, in real time.', t['uc_p_3'])
    content = content.replace('<div class="eyebrow">Languages</div>', f'<div class="eyebrow">{t["lang_eyebrow"]}</div>', 1)
    content = content.replace('<h2 class="section-title">Speak to anyone, anywhere</h2>', f'<h2 class="section-title">{t["lang_title"]}</h2>', 1)
    content = content.replace("Cosmo supports 70+ languages — from widely spoken to regional. A sample of what's available:", t['lang_sub'])
    content = content.replace('…and many more. Full list available in the app.', t['lang_more'])
    content = content.replace('Why do I need credits to translate?', t['faq_credits_q'])
    content = content.replace('Cosmo uses advanced AI models to deliver fast, accurate, and natural-sounding translations in real time. Unlike basic translation apps, every conversation is processed through these models which require computing power to run, and that has a cost. Credits are how we keep the service running while making sure you only pay for what you actually use. You can start for free with 20 guest credits, no account needed.', t['faq_credits_a'])
    return content

# ── Step 1: Create new language pages from EN ────────────────────────────────

with open(f'{base}/index.html', 'r', encoding='utf-8') as f:
    en_content = f.read()

for lang, t in translations.items():
    lang_dir = f'{base}/{lang}'
    os.makedirs(lang_dir, exist_ok=True)

    content = en_content

    # Set html lang attribute (and dir for Arabic)
    if t.get('rtl'):
        content = re.sub(r'<html lang="[^"]*"', f'<html lang="{t["html_lang"]}" dir="rtl"', content)
        # Add minimal RTL fix after existing style tag
        rtl_css = '''
    /* ─── RTL ─── */
    body { direction: rtl; text-align: right; }
    .nav-links { flex-direction: row-reverse; }
    .stats-bar { flex-direction: row-reverse; }
    .hero-actions { flex-direction: row-reverse; }'''
        content = content.replace('    /* ─── COMPARISON ─── */', rtl_css + '\n    /* ─── COMPARISON ─── */', 1)
    else:
        content = re.sub(r'<html lang="[^"]*"', f'<html lang="{t["html_lang"]}"', content)

    # Fix asset paths for subdirectory pages
    content = content.replace("url('assets/", "url('../assets/")
    content = content.replace('src="assets/', 'src="../assets/')

    # Apply translations
    content = apply_translation(content, t)

    # Update hreflang
    content = update_hreflang(content)

    # Update lang switcher (mark this language as selected)
    content = update_switcher(content, f'/{lang}/')

    with open(f'{lang_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {lang}/index.html')

# ── Step 2: Update existing pages (hreflang + switcher) ─────────────────────

existing = {
    f'{base}/index.html': ('/', 'en'),
    f'{base}/es/index.html': ('/es/', 'es'),
    f'{base}/fr/index.html': ('/fr/', 'fr'),
    f'{base}/zh/index.html': ('/zh/', 'zh'),
}

for path, (lang_value, html_lang) in existing.items():
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = update_hreflang(content)
    content = update_switcher(content, lang_value)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated: {path.replace(base + "/", "")}')

print('\nDone.')
