
def m_control_sph():
    from powderday.sph_tributary import sph_m_gen as m_gen
    return m_gen


def m_control_enzo():
    from powderday.enzo_tributary import enzo_m_gen as m_gen
    return m_gen



def ad_selector(ds):

    def sph_ad():
        return ds.all_data()

    def enzo_ad():
        #we don't return all_data here because ds/pf in enzo has
        #turned into a region object
        return ds
    
    ds_type = ds.dataset_type 
    #define the options dictionary
    options = {'gadget_hdf5':sph_ad,
               'tipsy':sph_ad,
               'enzo_packed_3d':enzo_ad}


    ad = options[ds_type]()
    return ad
