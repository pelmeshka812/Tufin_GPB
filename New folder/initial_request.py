def request():
    current_request = [['Другие администраторы', [['espi0108', '10.5.242.2', 'Sec-FW-API-I-ReadOnly'],
                                                  ['espi0109', '10.5.242.3', 'Sec-FW-API-I-ReadOnly'],
                                                  ['espi0110', '10.5.242.4', 'Sec-FW-API-I-ReadOnly']],
                        [['10.96.96.96', 'none'], ['10.96.96.97', 'none'], ['10.96.96.98', 'none']],
                        [['TCP, UDP', '514']], 'TCP, UDP', 'Тестовый комментарий второй'], ['Прикладные администраторы',
                                                                                            [['gpbu0105', '10.3.3.211',
                                                                                              'Sec-FW-API-D-AppAdm'],
                                                                                             ['gpbu0106', '10.2.2.201',
                                                                                              'Sec-FW-API-D-AppAdm'],
                                                                                             ['gpbu0107',
                                                                                              '172.16.2.220',
                                                                                              'Sec-FW-API-D-AppAdm']],
                                                                                            [['10.1.102.215', 'none'],
                                                                                             ['10.1.103.205', 'none'],
                                                                                             ['10.1.104.207', 'none']],
                                                                                            [['TCP', '445'],
                                                                                             ['TCP', 443], ['TCP', 22]],
                                                                                            'TCP\nHTTPS\nSSH',
                                                                                            'Тестовый комментарий первый'],
                       ['Прикладные администраторы', [['gpbu0105', '10.3.3.211', 'Sec-FW-API-D-AppAdm'],
                                                      ['gpbu0106', '10.2.2.201', 'Sec-FW-API-D-AppAdm'],
                                                      ['gpbu0107', '172.16.2.220', 'Sec-FW-API-D-AppAdm']],
                        [['192.168.100.229', 'none']], [['TCP', '1300'], ['TCP', '1400'], ['TCP', '1500']], 'TCP',
                        'Тестовый комментарий третий'], ['Тестовые сервера', [['10.1.102.215', 'none', 'none'],
                                                                              ['10.1.103.205', 'none', 'none'],
                                                                              ['10.1.104.207', 'none', 'none']],
                                                         [['192.168.100.229', 'none']], [['HTTPS', '443']], 'HTTPS',
                                                         'Тестовый комментарий третий']]
    return current_request
