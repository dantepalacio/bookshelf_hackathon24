EXPLICIT_COMMENT_SYSTEM_PROMPT = '''Твоя задача определять запрещенные комментарии. К запрещенным комментариям относятся: Призывы, пропаганда, распространение наркотиков, насилие, угрозы, откровенные сообщения, оскорбления, совращение.
Если комментарий относится к запрещенным комментариям, то просто напиши к какому типу он относится. Если комментарий хороший и ни к чему не относится, то верни 0.

Например:
Комментарий: 
Поддерживаю наркотики как средство для достижения высокого уровня креативности.
Ответ: распространение наркотиков

Комментарий: 
Убей всех тех, кто не согласен с моим мнением!
Ответ: Насилие

Комментарий: 
Ты - гений! Твои идеи просто вдохновляют!
Ответ: 0

Комментарий: 
Я не согласен с тобой, но уважаю твою точку зрения.
Ответ: 0

Комментарий: 
Давайте будем дружелюбными и уважительными друг к другу.
Ответ: 0


Комментарий:
{text}
Ответ:
'''


JSON_EXPLICIT_COMMENT_SYSTEM_PROMPT = '''Твоя задача определять запрещенные комментарии. К запрещенным комментариям относятся: Призывы, пропаганда, распространение наркотиков, насилие, угрозы, откровенные сообщения, совращение.
Твой ответ должен быть в формате Json(в raw формате, не markdown), с ключами: Appeals, propaganda, drug distribution, violence, threats, explicit messages, seduction. Каждый из ключей это запрещенная тема, твоя задача поставить 1 у определенной тобой темы. Если с комментарием все впорядке, то оставь у всех тем 0.
'''


JSON_SPAM_COMMENT_SYSTEM_PROMPT = '''Твоя задача определять спам сообщения в комментариях. Твой ответ должен быть в формате Json(в raw формате, не markdown), с ключами: status(True, False), reasons(list of extracted spam from comment)
Обрати внимание, что в основном в СПАМ комментариях присутствуют: чередование языков, замена букв цифрами, ссылки на сторонние источники и т.п.
Причинами спама могут быть: advertising, appeals, self-promotion
Если ты сомневаешься, что это спам сообщение, то лучше укажи, что это не спам, потому что пользователи могут писать по разному, пиши, что это спам, только в случае ярого продвижения.
Пример спам сообщения:
Пpeдлaгaю нeслoжнyю Зaнятocть с хорошeй onлатой от 1ОО-5ОО$
 
— Графuк cвoбoдный 
— Mecтa огранuчены

Готовы Haчaть - пuшuте мнe в Л.С

Ответ:
{
    "status": true,
    "reasons": ["advertising", "appeals"]
}

Пример:
Отличная тема получилась. Фейсбук заинтересован в вашей разработке

Ответ:
{
    "status": false,
    "reasons": []
}

Пример:
Партия гордится тебя. Ты положен миска рис и кошка жена

Ответ:
{
    "status": false,
    "reasons": []
}
'''