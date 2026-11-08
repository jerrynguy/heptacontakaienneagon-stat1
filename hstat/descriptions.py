"""Định nghĩa (mô tả) mặc định của 79 thuộc tính."""

DESCRIPTIONS: dict[str, str] = {
    'strength': (
        'Lực lớn nhất mà cơ bắp tạo ra được trong một lần gắng sức trọn vẹn, không xét đến thời '
        'gian cần để đạt tới mức lực đó. Quyết định khối lượng tối đa có thể nâng, đẩy, kéo, bẻ gãy '
        'hoặc ghì giữ: nhấc một tảng đá, giật tung cánh cửa gỗ, vật ngửa một con bò.'
    ),
    'endurance': (
        'Khoảng thời gian cơ thể giữ được hoạt động liên tục ở cường độ vừa phải trước khi kiệt '
        'quệ, tính trên quy mô nhiều giờ đến nhiều ngày. Thể hiện qua quãng đường hành quân trong '
        'một ngày, số giờ lao động không nghỉ, việc mang hành trang suốt một chuyến đi dài.'
    ),
    'agility': (
        'Khả năng đổi hướng, xoay người, dừng đột ngột rồi chuyển sang chuyển động khác một cách '
        'gọn gàng, gần như không mất đà. Thể hiện khi lách giữa đám đông, ngoặt gấp lúc đang chạy, '
        'leo qua mỏm đá hay nhảy qua nhiều chướng ngại liên tiếp trên địa hình gồ ghề.'
    ),
    'dexterity': (
        'Độ chính xác, tinh tế và nhuần nhuyễn của bàn tay và ngón tay khi thao tác với vật thể. '
        'Thể hiện qua việc xâu kim, thắt nút dây, mở ổ khóa bằng cây trâm, xoay con dao giữa các '
        'ngón, lấy đồ khỏi túi người khác mà họ không hay biết.'
    ),
    'speed': (
        'Vận tốc di chuyển tối đa của toàn thân trên một đường thẳng. Đo bằng thời gian cần để vượt '
        'qua một quãng đường cố định: chạy nước rút, lao tới một điểm, đuổi kịp hay bỏ xa kẻ khác '
        'trên đường bằng.'
    ),
    'reflexes': (
        'Độ trễ giữa lúc một kích thích bất ngờ xuất hiện (tiếng động, ánh chớp, cú chạm) và lúc cơ '
        'thể bắt đầu đáp lại, diễn ra tự động mà không cần suy nghĩ. Thể hiện khi chụp lấy vật đang '
        'rơi, giật tay khỏi lửa, nhắm mắt lại trước khi bụi kịp bay vào.'
    ),
    'flexibility': (
        'Biên độ chuyển động tối đa của các khớp và độ giãn của gân, dây chằng, mô mềm. Quyết định '
        'cơ thể có thể uốn cong, vặn xoắn, duỗi căng đến mức nào (xoạc chân, ngả lưng ra sau chạm '
        'đất, luồn người qua khe hẹp) mà không bị rách gân hay trật khớp.'
    ),
    'coordination': (
        'Khả năng điều phối nhiều bộ phận cơ thể hoạt động đồng thời và đúng trình tự để tạo ra một '
        'chuỗi động tác liền mạch. Thể hiện khi hai tay làm hai việc khác nhau cùng lúc, tay và '
        'chân giữ cùng một nhịp, hoặc nối nhiều cử động thành một tổ hợp trôi chảy như tung hứng '
        'hay nhảy múa.'
    ),
    'balance': (
        'Khả năng giữ trọng tâm cơ thể nằm vững trên chân đế để không ngã. Thể hiện khi đứng một '
        'chân, đi trên xà hẹp hay mặt băng trơn, trụ vững trên boong thuyền chòng chành, và lấy lại '
        'tư thế đứng khi trọng tâm bị xô lệch.'
    ),
    'explosive_power': (
        'Khả năng giải phóng một lượng lực lớn chỉ trong khoảnh khắc cực ngắn, tính bằng phần nhỏ '
        'của giây. Thể hiện qua cú bật nhảy cao, cú phóng người về phía trước, cú ném hay cú vung '
        'dứt khoát; đo bằng lượng lực đạt được chia cho thời gian để đạt được nó.'
    ),
    'hp': (
        'Tổng lượng tổn thương mà cơ thể có thể gánh trước khi gục ngã. Mỗi vết thương trừ dần vào '
        'quỹ này: còn nhiều thì vẫn đứng được dù mang đầy thương tích, cạn về 0 thì ngã xuống.'
    ),
    'stamina': (
        'Quỹ hơi sức ngắn hạn dành cho từng hành động gắng sức. Mỗi cú vung, cú nhảy, pha chạy gấp '
        'hay lần nhấc vật nặng tiêu hao một phần; khi cạn, cơ thể buộc phải dừng lại thở dốc vài '
        'giây để quỹ này tự đầy lại.'
    ),
    'recovery': (
        'Khả năng cơ thể tự lành lại các tổn hại một cách tự nhiên theo thời gian. Quyết định vết '
        'cắt khép miệng sau bao lâu, xương gãy liền lại sau bao nhiêu ngày, vết bầm tan đi sau mấy '
        'hôm và cơ thể trở lại trạng thái lành lặn sau bao lâu.'
    ),
    'pain_tolerance': (
        'Ngưỡng đau mà một người chịu được trước khi bị cơn đau chi phối hành động. Người có chỉ số '
        'cao vẫn cử động, cầm nắm và suy nghĩ bình thường khi đang mang vết thương nặng; cơn đau '
        'không khiến họ khựng lại, run rẩy, kêu la hay ngất đi.'
    ),
    'physical_resistance': (
        'Mức độ thân thể làm giảm thương tổn từ vật sắc, vật cùn và va chạm: chém, đâm, đập, va '
        'đập, rơi từ trên cao. Cùng một nhát chém, người có chỉ số cao chỉ bị rách da, người thấp '
        'có thể bị đứt lìa; đây là độ rắn chắc tự thân của da, thịt và xương.'
    ),
    'elemental_resistance': (
        'Mức độ thân thể làm giảm thương tổn do lửa, băng giá và sét gây ra. Quyết định da bị bỏng '
        'sâu hay chỉ ửng đỏ trước ngọn lửa, cơ thể bị tê cóng sau bao lâu trong giá lạnh, và cú '
        'giật điện để lại hậu quả nặng hay nhẹ.'
    ),
    'poison_resistance': (
        'Khả năng cơ thể trung hòa và đào thải chất độc đã lọt vào trong: nọc rắn, nọc nhện, thảo '
        'mộc độc, khí độc, chất tẩm trên lưỡi dao. Quyết định chất độc tích tụ chậm hay dồn dập, '
        'tác hại kéo dài bao lâu và cần liều lượng bao nhiêu mới đủ gây nguy hiểm.'
    ),
    'disease_resistance': (
        'Khả năng của hệ miễn dịch ngăn mầm bệnh (vi khuẩn, virus, ký sinh trùng, sự thối rữa) bám '
        'rễ và lan rộng trong cơ thể. Quyết định một người có bị lây khi ở giữa vùng dịch hay '
        'không, và nếu mắc thì bệnh nặng đến đâu.'
    ),
    'mental_resistance': (
        'Khả năng giữ cho ý thức của mình không bị xâm nhập hay chi phối bởi tác động từ bên ngoài: '
        'thôi miên, bùa mê, ảo ảnh, lời thì thầm gây điên loạn, kẻ đọc trộm hoặc cấy ý nghĩ vào '
        'đầu. Chỉ số cao giúp nhận ra ý nghĩ không phải của mình và đẩy nó ra trước khi bị nó dắt '
        'mũi.'
    ),
    'death_resistance': (
        'Khả năng cưỡng lại những hiệu ứng đoạt mạng tức thì vốn không tính đến lượng thương tích '
        '(lời nguyền tử thần, phép tức tử, ánh nhìn hóa đá), và khả năng níu giữ sự sống thêm một '
        'khoảnh khắc khi đã đứng ở ranh giới sống và chết.'
    ),
    'intelligence': (
        'Năng lực xử lý thông tin nền tảng của bộ óc: độ nhạy bén khi tiếp nhận một ý tưởng mới, '
        'khả năng nắm được khái niệm trừu tượng và theo kịp những lập luận phức tạp. Là dung lượng '
        'trí óc thuần, không gắn với một lĩnh vực cụ thể nào.'
    ),
    'perception': (
        'Độ nhạy và độ sắc nét của năm giác quan: thị giác, thính giác, khứu giác, vị giác, xúc '
        'giác. Quyết định chi tiết nhỏ nhất còn nhìn thấy, âm thanh khẽ nhất còn nghe ra, mùi nhạt '
        'nhất còn ngửi được và rung động nhẹ nhất còn cảm thấy trên da.'
    ),
    'awareness': (
        'Mức độ một người nắm được những gì đang diễn ra quanh mình tại mỗi thời điểm (có ai vừa '
        'bước vào, có gì vừa thay đổi, mối nguy nào đang hình thành), kể cả khi đang bận làm việc '
        'khác. Là bức tranh tình hình được cập nhật liên tục, giúp không bị bất ngờ trước biến cố.'
    ),
    'memory': (
        'Khả năng lưu giữ thông tin và gợi lại nó khi cần: gương mặt, tên gọi, lời nói, sự kiện, '
        'những nơi từng ghé qua. Bao gồm lượng thông tin giữ được, thời gian giữ được bao lâu và độ '
        'chính xác khi gợi lại.'
    ),
    'concentration': (
        'Khả năng dồn toàn bộ sự chú ý vào một việc duy nhất và giữ nó ở đó trong thời gian dài, '
        'không bị xao nhãng bởi tiếng ồn, chuyển động xung quanh hay ý nghĩ lan man. Thể hiện khi '
        'đọc sách, canh chừng một điểm hay làm việc tỉ mỉ hàng giờ liền mà không đứt mạch.'
    ),
    'learning_ability': (
        'Khả năng tiếp thu một điều hoặc một kỹ năng hoàn toàn mới. Đo bằng số lần cần quan sát, '
        'thực hành hoặc được chỉ dạy trước khi làm được việc chưa từng làm, và mức độ nắm được sau '
        'mỗi lần như vậy.'
    ),
    'analytical_thinking': (
        'Khả năng mổ xẻ một khối thông tin thành từng phần nhỏ, so sánh và đối chiếu chúng để tìm '
        'ra quy luật, điểm mâu thuẫn và mối quan hệ nhân quả. Thể hiện khi soi ra lời khai không '
        'khớp, tìm ra điểm chung giữa nhiều sự việc rời rạc hay xác định nguyên nhân gốc của một sự '
        'cố.'
    ),
    'problem_solving': (
        'Khả năng tìm ra lối thoát cho một tình huống bế tắc cụ thể: nghĩ ra nhiều phương án, chọn '
        'cách khả thi nhất với những gì đang có trong tay và biến nó thành hành động. Thể hiện khi '
        'mở một cánh cửa bị kẹt, vượt qua một câu đố, xoay xở khi thiếu đúng dụng cụ cần thiết.'
    ),
    'prediction': (
        'Khả năng ước đoán điều sẽ xảy ra tiếp theo từ những gì đang diễn ra trước mắt: diễn biến '
        'của một sự việc, hậu quả của một hành động, thời tiết sắp tới, hướng đi của dòng người. '
        'Thước đo là độ chính xác của lời đoán và khoảng thời gian có thể nhìn trước.'
    ),
    'spatial_awareness': (
        'Khả năng hình dung trong đầu hình dạng, kích thước, khoảng cách và vị trí tương đối của '
        'các vật thể trong ba chiều. Thể hiện khi ước lượng chính xác bức tường cao mấy mét, vật '
        'kia cách bao xa, một món đồ có lọt qua ô cửa không, hay hình dung được mặt sau của một vật '
        'chỉ thấy mặt trước.'
    ),
    'willpower': (
        'Lực đẩy nội tâm giúp bắt tay vào và ép bản thân hoàn thành một việc khó chịu ngay tại thời '
        'điểm này, dù bên trong đang trì hoãn, uể oải hay chán ngán. Là thứ khiến một người rời '
        'khỏi chỗ ấm để bước ra trời lạnh, hay bắt đầu một việc nặng nhọc ngay thay vì để mai.'
    ),
    'determination': (
        'Độ vững chắc của lời cam kết với một mục tiêu cụ thể đã chọn: mục tiêu đó luôn đứng ở vị '
        'trí số một trong lòng, không bị thay thế bởi lời can ngăn, sự hoài nghi của người khác hay '
        'một con đường dễ dàng hơn mở ra trước mắt.'
    ),
    'courage': (
        'Sự sẵn sàng chủ động tiến về phía hiểm nguy khi biết rõ cái giá có thể phải trả: xông vào '
        'ngôi nhà đang cháy, một mình bước ra đối mặt kẻ to lớn hơn, đứng chắn trước người yếu thế, '
        'nói thẳng sự thật trước kẻ có quyền.'
    ),
    'mental_fortitude': (
        'Khả năng của nội tâm đứng vững trước những đòn giáng nặng nề nhất của cuộc đời (mất người '
        'thân, bị phản bội, thất bại thảm hại, chứng kiến cảnh tàn khốc) mà không sụp đổ, tuyệt '
        'vọng hay mang vết hằn kéo dài nhiều năm.'
    ),
    'emotional_control': (
        'Khả năng điều tiết cường độ và sự bộc lộ của những gì mình đang cảm thấy (giận dữ, vui '
        'sướng, buồn bã, phấn khích) để nét mặt, giọng nói và phán đoán không bị cảm xúc nhất thời '
        'cuốn đi.'
    ),
    'stress_resistance': (
        'Khả năng giữ nguyên chất lượng làm việc khi bị dồn ép kéo dài: hạn chót cận kề, nhiều việc '
        'dồn dập cùng lúc, kỳ vọng nặng nề, hậu quả lớn nếu thất bại. Người có chỉ số cao vẫn ngủ '
        'được, ăn được và làm đúng việc giữa lúc mọi thứ căng như dây đàn.'
    ),
    'fear_resistance': (
        'Mức độ miễn nhiễm với cảm giác khiếp đảm. Chỉ số cao giúp không run rẩy, không đông cứng, '
        'không hoảng loạn bỏ chạy trước sinh vật quái dị, tiếng gầm rợn người, bóng tối, độ cao hay '
        'những hiệu ứng gieo nỗi sợ.'
    ),
    'self_control': (
        'Khả năng kìm lại một hành động mình đang thèm muốn làm (cơn thèm ăn uống, men say, lòng '
        'tham trước của cải, thôi thúc nhất thời) và chỉ hành động khi đã cân nhắc. Là chiếc phanh '
        'bên trong mỗi người.'
    ),
    'persistence': (
        'Khả năng quay lại thử tiếp sau mỗi lần thất bại, lặp đi lặp lại cùng một nỗ lực qua nhiều '
        'ngày, nhiều tháng cho đến khi đạt kết quả. Đo bằng số lần vấp ngã một người có thể trải '
        'qua mà vẫn đứng dậy làm lại.'
    ),
    'attack_power': (
        'Lượng sát thương thuần mà mỗi đòn đánh trúng đích gây ra cho mục tiêu. Là con số đầu ra '
        'của đòn đánh: cùng một cú trúng, chỉ số càng cao thì vết thương để lại càng sâu và mục '
        'tiêu bị tổn hại càng nặng.'
    ),
    'weapon_mastery': (
        'Mức độ thành thạo đối với từng loại vũ khí cụ thể: nắm rõ trọng lượng, tầm với, điểm cân '
        'của món đang cầm và khai thác trọn bộ chiêu thức đặc trưng của nó (kiếm, thương, rìu, '
        'cung, roi...). Một người có thể rất giỏi với kiếm nhưng vụng về với thương.'
    ),
    'combat_skill': (
        'Trình độ giao đấu nền tảng của chính người đánh: bộ pháp, giữ cự ly, nhịp ra đòn, nối '
        'chiêu, đánh tay không và kinh nghiệm thực chiến tích lũy qua từng trận. Áp dụng được dù '
        'đang tay không hay cầm bất cứ thứ gì.'
    ),
    'critical_ability': (
        'Khả năng biến một đòn đánh thường thành đòn chí mạng bằng cách đánh trúng chỗ hiểm (tim, '
        'cổ họng, khe giáp, sau gáy) khiến lượng sát thương tăng lên gấp bội. Quyết định cả tần '
        'suất ra được những đòn như vậy lẫn mức nhân thêm của chúng.'
    ),
    'parrying': (
        'Nghệ thuật đánh chệch hướng một đòn đang lao tới đúng khoảnh khắc nó sắp chạm người, bằng '
        'lưỡi kiếm, cán thương hay cổ tay bọc giáp, khiến lực đòn trượt đi và kẻ ra đòn mất đà, hớ '
        'hênh trong giây lát.'
    ),
    'blocking': (
        'Khả năng hứng trực diện đòn đánh bằng khiên, thân giáo hay cẳng tay bọc giáp, hấp thụ và '
        'dàn đều lực va chạm để phần thân phía sau không bị trúng. Quyết định lượng lực cản lại '
        'được mỗi lần và số đòn trụ được trước khi tấm chắn bị đánh bật khỏi tay.'
    ),
    'evasion': (
        'Khả năng đưa toàn thân ra khỏi quỹ đạo của đòn đánh hay vật phóng tới (lăn, lách, lùi, '
        'nhảy sang bên) để nó không chạm vào người. Chỉ số cao giúp thoát khỏi cả những đòn quét '
        'rộng lẫn những loạt tên bắn dồn dập.'
    ),
    'stance_breaking': (
        'Khả năng làm sụp đổ tư thế vững vàng của đối thủ bằng những đòn nặng dồn ép liên tiếp, cho '
        'đến khi họ lảo đảo, khuỵu gối, buông lỏng hai tay và để lộ toàn bộ sơ hở.'
    ),
    'counterattacking': (
        'Khả năng ra đòn đáp trả ngay vào khe hở mà đối phương vừa để lộ khi tung chiêu, chen vào '
        'đúng khoảnh khắc họ vung hụt, thu tay về hay chưa kịp lấy lại tư thế, biến lượt đánh của '
        'họ thành cơ hội của mình.'
    ),
    'tactical_awareness': (
        'Khả năng đọc cục diện của cả trận giao tranh và chọn cách đánh phù hợp: nhận ra kẻ địch '
        'nguy hiểm nhất, tận dụng địa hình, chọn chỗ đứng có lợi, quyết định lúc tiến, lúc lui, lúc '
        'giăng mồi nhử địch.'
    ),
    'combat_adaptability': (
        'Khả năng thay đổi lối đánh ngay giữa trận khi tình thế biến chuyển (đối phương đổi chiêu, '
        'môi trường xung quanh thay đổi, kế hoạch ban đầu đổ vỡ) và kịp thời tìm ra cách đối phó '
        'với kiểu kẻ địch chưa từng gặp.'
    ),
    'magic_intelligence': (
        'Năng lực lý trí dùng để nắm và vận hành ma pháp dựa trên công thức, nguyên lý và cấu trúc '
        'chặt chẽ. Quyết định độ phức tạp tối đa của phép mà người đó đủ trình độ sử dụng: chỉ số '
        'càng cao, những phép rắc rối càng nằm trong tầm với.'
    ),
    'faith': (
        'Sự gắn kết tâm linh với một đấng thiêng liêng hay một chân lý tối thượng, cho phép vay '
        'mượn quyền năng thần thánh qua lời cầu nguyện. Niềm tin càng sâu và thuần khiết thì những '
        'phép linh thiêng ở cấp càng cao càng được ban cho để sử dụng.'
    ),
    'arcane': (
        'Mối liên kết với tầng sâu bí ẩn và cấm kỵ của thế giới: vận mệnh, máu huyết, những thế lực '
        'cổ xưa bị lãng quên. Quyết định vận may khi bắt gặp vật phẩm hiếm và mức độ có thể khai mở '
        'các bí thuật u tối như huyết thuật hay nghi lễ cổ.'
    ),
    'fp': (
        'Lượng năng lượng nội tại dự trữ để chi trả cho mỗi lần dùng phép hay kích hoạt kỹ năng đặc '
        'biệt. Mỗi lần dùng trừ đi một phần; khi cạn thì không thể dùng thêm cho đến khi được nạp '
        'lại.'
    ),
    'sorcery_scaling': (
        'Hệ số nhân áp lên uy lực của các phép Sorcery, loại ma pháp dùng gậy phép làm vật dẫn. '
        'Cùng một phép Sorcery, hệ số càng cao thì lượng sát thương và cường độ hiệu ứng tạo ra '
        'càng lớn.'
    ),
    'incantation_scaling': (
        'Hệ số nhân áp lên uy lực của các phép Incantation, loại phép cầu khấn dùng thánh ấn làm '
        'vật dẫn. Cùng một phép Incantation, hệ số càng cao thì lượng sát thương và cường độ hiệu '
        'ứng tạo ra càng lớn.'
    ),
    'casting_speed': (
        'Thời gian từ lúc bắt đầu niệm cho đến khi phép được phóng ra, cùng khoảng nghỉ bắt buộc '
        'giữa hai lần dùng phép liên tiếp. Chỉ số càng cao, khoảng thời gian đứng yên trơ trọi khi '
        'niệm càng ngắn.'
    ),
    'spell_knowledge': (
        'Kho phép mà một người nắm trong tay: số lượng phép biết dùng, độ đa dạng các trường phái '
        'và chiều sâu hiểu biết về từng phép, kể cả khả năng nhận ra một phép lạ ngay khi thấy nó '
        'được dùng và biết được tác dụng của nó.'
    ),
    'spell_control': (
        'Độ chính xác và ổn định khi dẫn dắt một phép đã phóng ra: đánh trúng đúng điểm cần nhắm, '
        'định hình phạm vi và quỹ đạo theo ý muốn, giữ cho phép không phản phệ hay lan sang đồng '
        'đội.'
    ),
    'magical_resistance': (
        'Khả năng của thân thể làm tiêu tán ma thuật nhắm vào mình (tia sáng phép, quả cầu phép, '
        'luồng hắc thuật), giảm lượng sát thương mà các phép công kích loại này gây ra khi chạm tới '
        'người.'
    ),
    'summoning': (
        'Khả năng gọi linh hồn, sinh vật hay đồng minh từ nơi khác tới hiện diện bên cạnh để trợ '
        'giúp, và giữ chúng ở lại. Quyết định số lượng thực thể gọi được cùng lúc, cấp bậc của '
        'chúng và thời gian chúng tồn tại trước khi tan biến.'
    ),
    'crafting': (
        'Khả năng tự tay làm ra đồ dùng từ nguyên liệu thô thông thường như gỗ, da, vải, xương, '
        'sợi, lông vũ: mũi tên, dây thừng, túi da, quần áo, giỏ đựng, đồ ném và các vật phẩm tiêu '
        'hao. Đo bằng độ tinh xảo, độ hữu dụng của thành phẩm và lượng nguyên liệu hao phí.'
    ),
    'smithing': (
        'Kỹ năng nung, nện, tôi và gia công kim loại: làm ra lưỡi kiếm, mũi giáo, giáp trụ, đinh '
        'tán; mài sắc, gia cố và sửa lại đồ kim khí đã sứt mẻ. Quyết định độ cứng, độ sắc và tuổi '
        'thọ của sản phẩm làm ra.'
    ),
    'alchemy': (
        'Kỹ năng pha trộn, chưng cất, chiết xuất và biến đổi thảo mộc, khoáng vật, chất lỏng để tạo '
        'ra thuốc nước, bột nổ, dầu tẩm và các hợp chất có hiệu ứng đặc biệt. Bao gồm sự am hiểu về '
        'tính chất và tương tác giữa các chất, công thức và liều lượng pha chế.'
    ),
    'survival': (
        'Khả năng sống sót nơi hoang dã chỉ với những gì sẵn có: tìm nguồn nước sạch, nhóm lửa, '
        'dựng chỗ trú, phân biệt cây trái ăn được với thứ có hại, giữ ấm và trụ qua thời tiết khắc '
        'nghiệt.'
    ),
    'navigation': (
        'Khả năng xác định mình đang ở đâu trên một vùng đất rộng lớn và tìm đường đến đích: đọc '
        'bản đồ, dựa vào sao trời, mặt trời, dòng sông, dãy núi để giữ đúng lộ trình mà không bị '
        'lạc, kể cả ở nơi chưa từng đặt chân tới.'
    ),
    'tracking': (
        'Khả năng phát hiện và lần theo dấu vết mà một sinh vật để lại (vết chân, cành gãy, cỏ rạp, '
        'vệt máu, mùi hơi) để biết nó đã đi về phía nào, qua đây bao lâu rồi và có bao nhiêu cá '
        'thể.'
    ),
    'hunting': (
        'Kỹ năng hạ thú hoang để lấy thịt, da và nguyên liệu: nắm tập tính con mồi, rình rập, tiếp '
        'cận không gây động, giăng bẫy, hạ con mồi gọn bằng một phát, rồi xẻ thịt, lột da đúng '
        'cách.'
    ),
    'healing': (
        'Kỹ năng sơ cứu và điều trị cho bản thân và người khác: cầm máu, băng bó, nắn xương, khâu '
        'vết thương, đắp thuốc, chăm người ốm và dùng thuốc đúng liều. Quyết định một thương tích '
        'được xử lý đúng cách và nhẹ đi đến đâu sau khi qua tay người đó.'
    ),
    'engineering': (
        'Kỹ năng thiết kế, lắp ráp và vận hành cơ cấu máy móc: bánh răng, ròng rọc, đòn bẩy, lò xo, '
        'tời kéo, cầu treo, máy bắn đá, cửa sập. Bao gồm việc nắm nguyên lý lực và chuyển động để '
        'cỗ máy hoạt động đúng như dự tính.'
    ),
    'horsemanship': (
        'Kỹ năng ngồi vững và lèo lái thú cưỡi: đổi hướng bằng dây cương và gót chân, phi nước đại, '
        'nhảy qua hàng rào, vượt địa hình hiểm trở; kèm theo việc tạo sự gắn bó, chăm sóc và khiến '
        'con vật tin tưởng mình.'
    ),
    'charisma': (
        'Sức cuốn hút tự nhiên toát ra từ một người (phong thái, ánh mắt, giọng nói, sự hiện diện) '
        'khiến người khác chú ý, có thiện cảm và muốn ở gần ngay cả khi người đó chưa nói lời nào.'
    ),
    'persuasion': (
        'Khả năng dùng lý lẽ, bằng chứng và lời lẽ chọn lọc để khiến một người tự nguyện thay đổi '
        'quan điểm hoặc đồng ý làm điều mình đề nghị. Thước đo là mức độ người nghe thực sự bị lay '
        'chuyển chứ không chỉ gật đầu cho xong.'
    ),
    'leadership': (
        'Khả năng tập hợp, tổ chức và chỉ huy một nhóm người hướng tới mục tiêu chung: phân công '
        'đúng người đúng việc, ra mệnh lệnh rõ ràng, giữ kỷ luật và khiến cả nhóm hành động như một '
        'khối thống nhất, kể cả trong lúc hỗn loạn.'
    ),
    'deception': (
        'Khả năng che giấu ý định thật và khiến người khác tin vào điều sai: nói dối không để lộ sơ '
        'hở, giả vờ, đóng vai, cải trang, đánh lạc hướng, giữ vẻ mặt khớp hoàn toàn với lời nói.'
    ),
    'intimidation': (
        'Khả năng gây áp chế tâm lý lên người khác bằng ánh mắt, giọng nói, vóc dáng hay lời răn '
        'đe, khiến họ chùn bước, nhượng bộ, phục tùng hoặc khai ra điều mình muốn biết mà không cần '
        'động tay.'
    ),
    'diplomacy': (
        'Khả năng dàn xếp giữa các bên có lợi ích trái ngược nhau (đàm phán điều khoản, hòa giải '
        'bất đồng, giữ thể diện cho tất cả) để đi đến một thỏa thuận mà mọi bên đều chấp nhận được.'
    ),
    'reputation': (
        'Mức độ tên tuổi của một người được biết đến và cách thiên hạ nhìn nhận họ dựa trên những '
        'việc đã làm: kính trọng, tin cậy, e dè hay khinh miệt. Tiếng tăm này đi trước người đó, '
        'lan truyền qua lời kể tới những vùng đất họ chưa từng ghé.'
    ),
    'empathy': (
        'Khả năng cảm nhận trạng thái bên trong của người khác (niềm vui, nỗi buồn, nhu cầu, nỗi '
        'lo) như thể đặt mình vào vị trí của họ, và nhận ra cả những điều họ không nói thành lời.'
    ),
}
