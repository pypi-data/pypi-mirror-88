# code

data_labels = ['label', 'xcoord', 'ycoord', 'zcoord', 'vol', 's1', 's2', 's3', 'p1', 'p2', 'p3', 'peeq', 'sh', 'seq']
front_data_all = []
skipped_lines_all = []
for ip, path in enumerate(paths):
    if calc_bool[ip]:
        temp_ip = temps[ip] + 273
        front_data_all.append({
            'file_path': file_path,
            'data': {},
        })
        nodes_ip = front_coords_all[ip][0]
        elements_ip = front_coords_all[ip][1]
        nsets_ip = front_coords_all[ip][2]

        nodes_front = {
            'index': [],
        }
        elements_front = {
            'index': [],
            'nodal connectivity': []
        }
        good_idx = np.where(np.isin(nodes_ip['index'], nsets_ip[front_name]))[0]
        nodes_front['coord'] = nodes_ip['coord'][good_idx].squeeze()
        nodes_front['index'] = nsets_ip[front_name]

#         print('nodes_front', nodes_front)
        # # find elements with 2 nodes that belong to above set 
        for row_idx, i in enumerate(elements_ip['nodal connectivity']):
            isin = np.isin(i, nodes_front['index'])
#             print(isin)
            if row_idx == 2:
                print(np.sum(isin))
            if np.sum(isin) == 4:
        #         print('good row idx: {}'.format(row_idx))
                elements_front['index'].append(elements_ip['index'][row_idx])
                elements_front['nodal connectivity'].append(i)
                
        num_front_elem = len(np.array(elements_front['index'])) // num_layers[ip]

        elements_front['index'] = np.array(elements_front['index'])[0:num_front_elem]
        elements_front['nodal connectivity'] = np.array(elements_front['nodal connectivity'])[0:num_front_elem]

        curr_line = 0
        skipped_lines = 0
        front_data_all[ip]['data'] = []
        curr_line += 1
        labels_0 = pd.Series(dtype=np.float)
        data_0 = 0
            
        for file_path in glob.iglob(path+'\ehis*'):
            print(file_path)
            with open(file_path, 'rb') as file:
                line = file.readline()

            frame_i, num_elem_i = [int(n) for n in line.strip().split()]
            if num_elem_i == 0:
                skipped_lines += 1
            elif num_elem_i > 0:
                data_i = pd.read_csv(file_path, delim_whitespace=True, skiprows=1, index_col=False,
                                                 nrows=num_elem_i, names=data_labels)
                labels_i = data_i['label']
                front_labels_i_idx = np.where(np.isin(labels_i, elements_front['index']))[0]

                if len(front_labels_i_idx)>0:
    #                     print('front_labels_i_idx: ', front_labels_i_idx)
                    pl_elem_check = labels_i.isin(labels_0)
                    x_i = data_i['xcoord'].values
                    y_i = data_i['ycoord'].values
                    smin_i = np.min(data_i[['s1', 's2', 's3']], axis=1)
                    smax_i = np.max(data_i[['s1', 's2', 's3']], axis=1)
                    pmax_i = np.max(data_i[['p1', 'p2', 'p3']], axis=1)
                    if 'blm' in path:
                        vols_i = data_i['vol'] * 1e9
                    else:
                        vols_i = data_i['vol']

                    peeq_i = data_i['peeq']
                    sh_i = data_i['sh']
                    seq_i = data_i['seq']
                    tau_i = (smax_i - smin_i) / 2
                    thinf_i = thinf(dbrack, tau_i, temp_ip)


    #                     smax_i_allt = smax_i.copy()
    #                     smax_i_allt[labels_i.isin(labels_0)] = np.max([smax_0.values[np.where(labels_0.isin(labels_i))], 
    #                                                               smax_i_allt[labels_i.isin(labels_0)].values], axis=0)

                    peeq_0 = np.zeros(len(labels_i))

                    front_data_all[ip]['data'].append({
                        'frame_i': frame_i,
                        'num_elem_i': num_elem_i,
                        'elem_labels': labels_i[front_labels_i_idx],
                        'xcoord': x_i[front_labels_i_idx] - x_i[front_labels_i_idx][0],
                        'ycoord': y_i[front_labels_i_idx] - y_i[front_labels_i_idx][0],
                        'smax': smax_i[front_labels_i_idx],
                        'smin': smin_i[front_labels_i_idx],
    #                         'smaxallt': smax_i_allt[front_labels_i_idx],
                        'vol': vols_i[front_labels_i_idx],
                        'peeq': peeq_i[front_labels_i_idx],
                        'thinf': thinf_i[front_labels_i_idx],
                    })


                labels_0 = labels_i.copy()
    #                     smax_0 = smax_i_allt.copy()
                data_0 = data_i
        skipped_lines_all.append(skipped_lines)
