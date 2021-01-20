import pandas as pd

class parse_excel_table:
    def parse_excel_table_template(self):
        # Loading excel file and parsing sheets
        csv = pd.ExcelFile('Pass_Table_Template_v.1.7.xlsx')
        passage_table = csv.parse('Таблица проходов', header=1)
        passage_table = passage_table.iloc[3:]
        server_groups = csv.parse('Группы серверов', header=1)
        apm_groups = csv.parse('Группы АРМ польз. и админ.', header=1)
        ad_access_group = csv.parse('Группы доступа AD', header=1)
        

        # Selecting columns C, D, G, H, I, J, K & L where column Internal Sources is not null
        selected_rows = passage_table[['Internal sources', 'Internal sources segment type', 'Internal destination',
                                    'Internal destination segment type', 'Protocol/Service', 'Port', 'Comment', 'Status']][(passage_table['Internal sources'].notna())]

        rejected_list = []
        access_roles = []
        access_roles_apm = []
        access_roles_iterate = []
        access_roles_pre_iterate = []

        # Iterating over rows in Sheet 1 passage table
        for index, row in selected_rows.iterrows():

            # Looking for null values in required columns and droping them from filtered dataframe (selected_rows)
            if pd.isnull(row).values.any():
                rejected_list.append(row['Internal sources'])
                selected_rows = selected_rows.drop(index)

        # Iterating over rows in Sheet 3 for fixing merged cells
        i = 0
        grp = ''
        for index, row in apm_groups.iterrows():
            if type(row['№']) == float and pd.isna(row['№']):
                apm_groups.at[index, '№'] = i
                apm_groups.at[index,
                            'Название группы\n\nВнимательно прочитайте примечание к ячейке'] = grp
            else:
                i = row['№']
                grp = row['Название группы\n\nВнимательно прочитайте примечание к ячейке']
            # print(row)
        apm_groups.rename(columns={
            'Название группы\n\nВнимательно прочитайте примечание к ячейке': 'Internal sources'}, inplace=True)
        # Filtering matching values from Sheet 1 and 3
        result_source_access_roles = selected_rows.merge(apm_groups, on='Internal sources', how='inner').drop(['Internal sources segment type', 'Internal destination', 'Internal destination segment type',
                                                                                                            'Protocol/Service', 'Port', 'Comment', 'Status', '№', 'ФИО участника группы\n\nВнимательно прочитайте примечание к ячейке', 'Наименование ССП участника группы'], axis=1)

        # Iterating over rows in Sheet 2 for fixing merged cells
        i = 0
        grp = ''
        server_groups.rename(columns={
            'Название группы\n\nВнимательно прочитайте примечание к ячейке': 'Internal sources'}, inplace=True)
        for index, row in server_groups.iterrows():
            if type(row['№']) == float and pd.isna(row['№']):
                server_groups.at[index, '№'] = i
                server_groups.at[index, 'Internal sources'] = grp
            else:
                i = row['№']
                grp = row['Internal sources']

        # Merging common Internal Sources in sheet 1 & 2
        result_source_servers_ip = selected_rows.merge(server_groups, on='Internal sources', how='inner').drop(
            ['Internal sources segment type', 'Internal destination', 'Internal destination segment type', 'Protocol/Service', 'Port', 'Comment', 'Status', '№', 'DNS имя сервера, входящего в группу', 'Краткое описание сервера, входящего в группу'], axis=1)

        #Checking for not found sources
        not_found = []
        list_not_found = selected_rows[['Internal sources']].values.tolist()
        list_access_roles = result_source_access_roles[[
            'Internal sources']].values.tolist()
        list_servers_ip = result_source_servers_ip[[
            'Internal sources']].values.tolist()
        for nf in list_not_found:
            if nf not in list_access_roles:
                if nf not in list_servers_ip:
                    not_found.append(nf)

        # Looking for internal destinatoin from sheet 1 in sheet 2
        server_groups.rename(columns={
            'Internal sources': 'Internal destination'}, inplace=True)
        result_destination_servers_ip = server_groups.merge(selected_rows, on='Internal destination', how='left').drop(
            ['№', 'DNS имя сервера, входящего в группу', 'Краткое описание сервера, входящего в группу', 'Internal sources segment type', 'Internal destination segment type', 'Protocol/Service', 'Port', 'Comment', 'Status'], axis=1)
        server_groups.rename(columns={
            'Internal destination': 'Internal sources'}, inplace=True)
        result_destination_servers_ip.rename(columns={
            'IP адрес сервера, входящего в группу\n\nВнимательно прочитайте примечание к ячейке': 'IP'}, inplace=True)

        #Checking for not found destinations
        result_destination_not_found = selected_rows[['Internal destination']]

        for index, row in result_destination_not_found.iterrows():
            if row['Internal destination'] in result_destination_servers_ip['Internal destination'].values:
                result_destination_not_found = result_destination_not_found.drop(
                    index)

        # Creating list for sources
        int_src = ''
        for index, row in result_source_access_roles.iterrows():
            if int_src != row['Internal sources']:
                access_roles_iterate.append(access_roles_pre_iterate)
                access_roles_pre_iterate = []
                access_roles.append(access_roles_iterate)
                access_roles_iterate = []
                access_roles_iterate.append(row['Internal sources'])
                int_src = row['Internal sources']
                access_roles_apm.append(row['Имя учетной записи участника группы'])
                access_roles_apm.append(
                    row['IP адрес рабочей станции участника группы'])
                access_roles_pre_iterate.append(access_roles_apm)
                access_roles_apm = []
            else:
                access_roles_apm.append(row['Имя учетной записи участника группы'])
                access_roles_apm.append(
                    row['IP адрес рабочей станции участника группы'])
                access_roles_pre_iterate.append(access_roles_apm)
                access_roles_apm = []
        access_roles_iterate.append(access_roles_pre_iterate)
        access_roles.append(access_roles_iterate)

        access_roles = [item for item in access_roles if item != []]

        int_src = ''
        access_roles_iterate = []
        access_roles_pre_iterate = []
        for index, row in result_source_servers_ip.iterrows():
            if int_src != row['Internal sources']:
                access_roles_iterate.append(access_roles_pre_iterate)
                access_roles_pre_iterate = []
                access_roles.append(access_roles_iterate)
                access_roles_iterate = []
                access_roles_iterate.append(row['Internal sources'])
                int_src = row['Internal sources']
                access_roles_apm.append(
                    row['IP адрес сервера, входящего в группу\n\nВнимательно прочитайте примечание к ячейке'])
                access_roles_apm.append('none')
                access_roles_pre_iterate.append(access_roles_apm)
                access_roles_apm = []
            else:
                access_roles_apm.append(
                    row['IP адрес сервера, входящего в группу\n\nВнимательно прочитайте примечание к ячейке'])
                access_roles_apm.append('none')
                access_roles_pre_iterate.append(access_roles_apm)
                access_roles_apm = []
        access_roles_iterate.append(access_roles_pre_iterate)
        access_roles.append(access_roles_iterate)
        access_roles = [item for item in access_roles if item != [[]]]

        # Adding destinations to access_roles list
        int_src = ''
        int_dest = ''
        access_roles_apm = []
        access_roles_iterate = []
        access_roles_pre_iterate = []
        access_roles_dest = []
        for index, row in result_destination_servers_ip.iterrows():

            if int_dest != row['Internal destination'] and int_src != row['Internal sources']:
                access_roles_iterate.append(access_roles_pre_iterate)
                access_roles_pre_iterate = []
                access_roles_dest.append(access_roles_iterate)
                access_roles_iterate = []
                access_roles_iterate.append(row['Internal sources'])
                int_dest = row['Internal destination']
                int_src = row['Internal sources']
                access_roles_apm.append(row['IP'])
                access_roles_apm.append('none')
                access_roles_pre_iterate.append(access_roles_apm)
                access_roles_apm = []
            elif int_dest == row['Internal destination'] and int_src == row['Internal sources']:
                access_roles_apm.append(row['IP'])
                access_roles_apm.append('none')
                access_roles_pre_iterate.append(access_roles_apm)
                access_roles_apm = []
            else:
                access_roles_iterate.append(access_roles_pre_iterate)
                access_roles_pre_iterate = []
                access_roles_dest.append(access_roles_iterate)
                access_roles_iterate = []
                access_roles_iterate.append(row['Internal sources'])
                int_dest = row['Internal destination']
                int_src = row['Internal sources']
                access_roles_apm.append(row['IP'])
                access_roles_apm.append('none')
                access_roles_pre_iterate.append(access_roles_apm)
                access_roles_apm = []
        access_roles_iterate.append(access_roles_pre_iterate)
        access_roles_dest.append(access_roles_iterate)
        access_roles_dest = [item for item in access_roles_dest if item != [[]]]

        access_roles_df = pd.DataFrame(access_roles)
        access_roles_df.columns = ['Internal sources', 'Source addresses']

        access_roles_dest_df = pd.DataFrame(access_roles_dest)
        access_roles_dest_df.columns = [
            'Internal sources', 'Destination addresses']

        result_df = access_roles_df.merge(
            access_roles_dest_df, on='Internal sources', how='left')
        result_df = result_df.merge(selected_rows, on='Internal sources', how='left').drop(
            ['Status', 'Internal destination', 'Internal destination segment type', 'Internal sources segment type', 'Port'], axis=1)

        # Adding Protocol/Services
        protocol_list = []
        pre_protocol_list = []
        pre_protocol_list_1 = []
        for index, row in result_df.iterrows():
            pre_protocol_list_1 = row['Protocol/Service'].split('\n')
            int_src = row['Internal sources']
            pre_protocol_list.append(int_src)
            pre_protocol_list.append(pre_protocol_list_1)
            protocol_list.append(pre_protocol_list)
            pre_protocol_list = []
            pre_protocol_list_1 = []
        protocol_list_df = pd.DataFrame(protocol_list)
        protocol_list_df.columns = [
            'Internal sources', 'Services']

        result_df = result_df.merge(protocol_list_df, on='Internal sources', how='left').drop(
            ['Protocol/Service'], axis=1)
        result_df = result_df[['Internal sources', 'Source addresses',
                            'Destination addresses', 'Services', 'Comment']]
        result_set = result_df.values.tolist()
        return result_set

f = open('text.xlrd', 'w')
f.write(' '.join(str(parse_excel_table())))
