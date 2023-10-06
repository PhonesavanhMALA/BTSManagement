import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import operator
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains



def AddingBTS():
    URL = 'http://ictdemo1.etllao.com/bts-new/login.php'
    # open Chrome
    chrome_driver_path = "./chromedriver"
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    OpenWebSite = driver.get(URL)
    driver.maximize_window()
    time.sleep(0.6)
    ### Check status of webiste
    statusCode = requests.get(URL)
    statusCode = statusCode.status_code
    print(statusCode)
    BTSWeb_Wait03 =  driver.implicitly_wait(3)
    BTSWeb_Wait05 =  driver.implicitly_wait(5)
    BTSWeb_Wait1 =  driver.implicitly_wait(5)


    #### Read data from excel
    MAINDATA = pd.read_excel('./01AddingSiteName.xlsx', dtype=str)
    print(MAINDATA)
    

    ### Check if status == 200
    statusCode = 200
    if statusCode == 200:
        L_SiteName_EN = list(set(MAINDATA['SiteName'].tolist()))
        print(L_SiteName_EN)
        
        # assert "Python" in driver.title
        Input_Username = driver.find_element(By.NAME, "username")
        Input_Password = driver.find_element(By.NAME, "password")
        Input_Username.clear()
        Input_Password.clear()
        Input_Username.send_keys("Admin")
        Input_Password.send_keys("123")
        
        ### Search Submit Login
        submit_Login = driver.find_element(By.NAME, "login")
        HomePage = submit_Login.click()
        BTSWeb_Wait05
        
        
        # FSite.send_keys("103Hospital-L2600")
        i = 0
        for site in L_SiteName_EN:
            print("PRINT SITE:::::::::::")
            print(site)
            ### Go to Site page
            SitePage =  driver.find_element_by_xpath("/html/body/nav/div/ul/li[2]/a").click()
            ### Find site by name
            FSite = driver.find_element(By.NAME, "sitename").send_keys(site)
            ### Click Search
            Click_Search = driver.find_element(By.ID, "search").click()
            ### Count Rows of table
            rows = driver.find_elements_by_xpath("/html/body/div/div/form[2]/div[1]/table/tbody/tr")
            numOfRows = int(len(rows))
            
            
            Current_MAINDATA = pd.DataFrame()
            Current_MAINDATA = MAINDATA[MAINDATA['SiteName'] == site]
            Current_MAINDATA.sort_values(by='BTS(ID)', ascending=True)
            print(Current_MAINDATA)
            Get_SiteName_LA = Current_MAINDATA[Current_MAINDATA['SiteName']==site]['Laos SiteName'].values[0]
            Get_Province = Current_MAINDATA[Current_MAINDATA['SiteName']==site]['Province'].values[0]
            Get_District = Current_MAINDATA[Current_MAINDATA['SiteName']==site]['District'].values[0]
            Get_BTSID = list(set(Current_MAINDATA[Current_MAINDATA['SiteName']==site]['BTS(ID)'].tolist()))
            Get_BTSID.sort()
            print("After sorted")
            print(Get_BTSID)
            if numOfRows > 0:
                driver.implicitly_wait(5)
                ### Select province and distrct
                selectProvince = driver.find_element_by_css_selector("#prov_id_s").send_keys(Get_Province)
                selectDistrict = driver.find_element_by_css_selector("#district_id").send_keys(Get_District)
                ### Click Search
                Click_Search = driver.find_element(By.ID, "search").click()
                ### Count Rows of table
                rows = driver.find_elements_by_xpath("/html/body/div/div/form[2]/div[1]/table/tbody/tr")
                numOfRows = int(len(rows))
                pass
            print(len(rows))
            if numOfRows == 0:
                driver.implicitly_wait(5)
                ### >>>>>> Adding Site
                SiteName = L_SiteName_EN[i]
                LaoSiteName = Get_SiteName_LA
                Province = Get_Province
                District = Get_District
                ### Adding New sitename
                ClickADD = driver.find_element_by_id("addBTS")
                ClickADD.click()
                #### English site
                SelectSiteNameEN = driver.find_element_by_name("site_name_en[]")
                SelectSiteNameEN.click()
                SelectSiteNameEN.send_keys(SiteName)
                #### Lao site
                SelectSiteNameLA = driver.find_element_by_name("site_name_la[]")
                SelectSiteNameLA.click()
                SelectSiteNameLA.send_keys(LaoSiteName)
                BTSWeb_Wait05
                #### Province
                DropProvince=Select(driver.find_element_by_id("prov_id"))
                DropProvince.select_by_visible_text(Province)
                BTSWeb_Wait05
                #### District
                DropDistrict = Select(driver.find_element_by_name("dist_id[]"))
                DropDistrict.select_by_visible_text(District)
                BTSWeb_Wait05
                #### Save siteName
                btnSave = driver.find_element_by_name("btnsave")
                btnSave.click()
                driver.switch_to.alert.accept()
                BTSWeb_Wait05
                
                
                
                ### Add BTS ID
                ### refresh page
                driver.refresh()
                BTSWeb_Wait1
                btn_Plus = driver.find_element_by_xpath("/html/body/div/div/form[2]/div[1]/table/tbody/tr[1]/td[8]")
                btn_Plus.click()
                BTSWeb_Wait1
                btn_AddNew = driver.find_element_by_id("addBTS").click()
                for btsid in Get_BTSID:
                    ### Count Rows of table
                    CurrentRows = driver.find_elements_by_xpath("/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr")
                    numOf_CurrentRows= int(len(CurrentRows))
                    getFirstNumber = int(btsid[0])
                    ### Check 2G BTS ID
                    if getFirstNumber == 1:
                        ### get information
                        SiteID = btsid
                        LAC_TAC = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['LAC_TAC'].values[0]
                        btsType = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['BTS Type'].values[0]
                        frequency = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Frequency'].values[0]
                        controllType = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Controller Type'].values[0]
                        vendor = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Vendor'].values[0]
                        status = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Status'].values[0]
                        getCells = len(Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID])
                        print(getCells)
                        BTSWeb_Wait05
                        ### input information
                        addSiteID = driver.find_element_by_css_selector(f"body > div > div > form > div > div.panel-body > div.row.table-responsive > table > tbody > tr:nth-child({numOf_CurrentRows}) > td:nth-child(2) > input").send_keys(SiteID)
                        BTSWeb_Wait05                        
                        # create action chain object
                        action = ActionChains(addSiteID)                
                        # perform the operation
                        HitTab = action.key_down(Keys.TAB)
                        BTS_TYPE = Select(driver.find_element_by_css_selector("#tech_type")).select_by_visible_text(btsType)
                        addFrequency = Select(driver.find_element_by_css_selector("#freq")).select_by_visible_text(frequency)
                        addControllType = Select(driver.find_element_by_xpath(f"/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr[{numOf_CurrentRows}]/td[5]/select")).select_by_visible_text(controllType)
                        addLACTAC = driver.find_element_by_xpath(f"/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr[{numOf_CurrentRows}]/td[6]/input").send_keys(LAC_TAC)
                        addVendor = Select(driver.find_element_by_css_selector("#vendor_id")).select_by_visible_text(vendor)
                        addStatus = Select(driver.find_element_by_name("status[]")).select_by_visible_text(status)
                        
                        #### SAVE DATA
                        btnSAVECell = driver.find_element_by_name("btnsave").click()
                        driver.switch_to.alert.accept()
                        driver.refresh()
                        BTSWeb_Wait1
                        
                        #### Add cell to 2G
                        if getCells >= 1:
                            getListCellCode = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Cell ID'].tolist()
                            getListCI = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['CI_PCI'].tolist()
                            getListFrequency = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Frequency'].tolist()
                            getListStatus = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Status'].tolist()
                            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                            get_CurrentRowsBTS = driver.find_elements_by_xpath("/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr")
                            numOf_CurrentRows= int(len(get_CurrentRowsBTS))
                            ### Click Edit BTS Cell inside BTS
                            ClickEditBTS = driver.find_element_by_xpath(f"/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr[1]/td[9]").click()
                            if numOf_CurrentRows > 0:
                                j = 0
                                cellNum = 1                         
                                for cellCode in getListCellCode:                                                 
                                    print(f"HI i'm CELLNUM:::::::::::::::;; {cellNum}")
                                    # BTSWeb_Wait05
                                    # get_CurrentRowsBTS = driver.find_elements_by_xpath("/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr")
                                    # numOf_CurrentRows= int(len(get_CurrentRowsBTS))
                                    ### ADD CELLS to BTS
                                    ### click add new to add cell
                                    BTSWeb_Wait1
                                    btnNewCell = driver.find_element_by_css_selector('#addBTS').click()
                                    BTSWeb_Wait03                                  
                                    addCellCode = driver.find_element_by_xpath(f"/html/body/div/div/form/div[4]/table/tbody/tr[{cellNum}]/td[3]/input").send_keys(cellCode)
                                    BTSWeb_Wait03
                                    addCI_PCI= driver.find_element_by_xpath(f"/html/body/div/div/form/div[4]/table/tbody/tr[{cellNum}]/td[4]/input").send_keys(getListCI[j])
                                    BTSWeb_Wait03
                                    addFrequency= driver.find_element_by_xpath(f"/html/body/div/div/form/div[4]/table/tbody/tr[{cellNum}]/td[5]/select").send_keys(getListFrequency[j])
                                    BTSWeb_Wait05
                                    addStatus= driver.find_element_by_xpath(f"/html/body/div/div/form/div[4]/table/tbody/tr[{cellNum}]/td[6]/select").send_keys(getListStatus[j])
                                    BTSWeb_Wait05
                                    #### SAVE DATA
                                    btnSAVECell = driver.find_element_by_name("btnsave").click()
                                    driver.switch_to.alert.accept()
                                    driver.refresh()
                                    j+=1
                                    cellNum += 1
                                    BTSWeb_Wait1
                        BTSWeb_Wait1
                    elif getFirstNumber == 4:
                        ### Go to Site page
                        SitePage4G =  driver.find_element_by_xpath("/html/body/nav/div/ul/li[2]/a").click()
                        ### Find site by name
                        FSite4G = driver.find_element(By.NAME, "sitename").send_keys(site)
                        ### Click Search
                        Click_Search4G = driver.find_element(By.ID, "search").click()
                        ### Count Rows of table
                        rows4G = driver.find_elements_by_xpath("/html/body/div/div/form[2]/div[1]/table/tbody/tr")
                        numOfRows4G = int(len(rows4G))
                        print(numOfRows4G)
                        if numOfRows4G == 0:
                            ### add information from the begining
                            pass
                        elif numOfRows4G == 1:
                            ### Add only 4G
                            ### Add BTS ID
                            driver.refresh()
                            BTSWeb_Wait05
                            btn_Plus = driver.find_element_by_xpath("/html/body/div/div/form[2]/div[1]/table/tbody/tr[1]/td[8]").click()
                            BTSWeb_Wait05
                            btn_AddNew = driver.find_element_by_id("addBTS").click()
                            ### Count Rows of table
                            CurrentRows = driver.find_elements_by_xpath("/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr")
                            numOf_CurrentRows= int(len(CurrentRows))
                            ### get information
                            SiteID = btsid
                            LAC_TAC = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['LAC_TAC'].values[0]
                            btsType = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['BTS Type'].values[0]
                            frequency = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Frequency'].values[0]
                            controllType = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Controller Type'].values[0]
                            vendor = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Vendor'].values[0]
                            status = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Status'].values[0]
                            getCells = len(Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID])
                            print(getCells)
                            
                            ### input information
                            addSiteID = driver.find_element_by_css_selector(f"body > div > div > form > div > div.panel-body > div.row.table-responsive > table > tbody > tr:nth-child({numOf_CurrentRows}) > td:nth-child(2) > input").send_keys(SiteID)
                            BTSWeb_Wait05                        
                            # create action chain object
                            action = ActionChains(addSiteID)                
                            # perform the operation
                            HitTab = action.key_down(Keys.TAB)
                            BTS_TYPE = Select(driver.find_element_by_css_selector("#tech_type")).select_by_visible_text(btsType)
                            BTSWeb_Wait03
                            HitTab = action.key_down(Keys.TAB)
                            addFrequency = Select(driver.find_element_by_xpath(f"/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr[{numOf_CurrentRows}]/td[4]/select")).select_by_visible_text(frequency)
                            BTSWeb_Wait03
                            CheckControtype = str(controllType)[0].upper()
                            if CheckControtype.startswith("N"):
                                pass
                            else:
                                addControllType = Select(driver.find_element_by_xpath(f"/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr[{numOf_CurrentRows}]/td[5]/select")).select_by_visible_text(controllType)
                            BTSWeb_Wait03
                            addLACTAC = driver.find_element_by_xpath(f"/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr[{numOf_CurrentRows}]/td[6]/input").send_keys(LAC_TAC)
                            BTSWeb_Wait03
                            addVendor = Select(driver.find_element_by_css_selector("#vendor_id")).select_by_visible_text(vendor)
                            BTSWeb_Wait03
                            addStatus = Select(driver.find_element_by_name("status[]")).select_by_visible_text(status)
                            BTSWeb_Wait03
                            #### SAVE DATA
                            btnSAVECell = driver.find_element_by_name("btnsave").click()
                            driver.switch_to.alert.accept()
                            driver.refresh()
                            BTSWeb_Wait1
                            driver.refresh()
                            BTSWeb_Wait1
                            
                            #### Add cell to 4G
                            if getCells >= 1:
                                getListCellCode = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['CellCode'].tolist()
                                getListCellPort = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Cell ID'].tolist()
                                getListCI = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['CI_PCI'].tolist()
                                getListFrequency = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Frequency'].tolist()
                                getListStatus = Current_MAINDATA[Current_MAINDATA['BTS(ID)']==SiteID]['Status'].tolist()
                                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                                get_CurrentRowsBTS = driver.find_elements_by_xpath("/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr")
                                numOf_CurrentRows= int(len(get_CurrentRowsBTS))
                                ### Click Edit BTS Cell inside BTS
                                ClickEdit4G = driver.find_element_by_xpath(f"/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr[{numOf_CurrentRows}]/td[9]").click()
                                if numOf_CurrentRows > 0:
                                    j = 0
                                    cellNum = 1                         
                                    for cellCode in getListCellCode:                                                 
                                        print(f"HI i'm CELLNUM:::::::::::::::;; {cellNum}")
                                        BTSWeb_Wait05
                                        # get_CurrentRowsBTS = driver.find_elements_by_xpath("/html/body/div/div/form/div/div[2]/div[3]/table/tbody/tr")
                                        # numOf_CurrentRows= int(len(get_CurrentRowsBTS))
                                        ### ADD CELLS to BTS
                                        ### click add new to add cell
                                        btnNewCell = driver.find_element_by_css_selector('#addBTS').click()                                    
                                        BTSWeb_Wait03
                                        addCellCode = driver.find_element_by_xpath(f"/html/body/div/div/form/div[4]/table/tbody/tr[{cellNum}]/td[3]/input").send_keys(cellCode)
                                        BTSWeb_Wait03
                                        addCellPort = driver.find_element_by_xpath(f"/html/body/div/div/form/div[4]/table/tbody/tr[{cellNum}]/td[4]/input").send_keys(getListCellPort[j])
                                        BTSWeb_Wait03
                                        addCI_PCI= driver.find_element_by_xpath(f"/html/body/div/div/form/div[4]/table/tbody/tr[{cellNum}]/td[5]/input").send_keys(getListCI[j])
                                        BTSWeb_Wait03
                                        addFrequency= driver.find_element_by_xpath(f"/html/body/div/div/form/div[4]/table/tbody/tr[{cellNum}]/td[6]/select").send_keys(getListFrequency[j])
                                        BTSWeb_Wait03
                                        addStatus= driver.find_element_by_xpath(f"/html/body/div/div/form/div[4]/table/tbody/tr[{cellNum}]/td[7]/select").send_keys(getListStatus[j])
                                        BTSWeb_Wait05
                                        #### SAVE DATA
                                        btnSAVECell = driver.find_element_by_name("btnsave").click()
                                        driver.switch_to.alert.accept()
                                        BTSWeb_Wait1
                                        driver.refresh()
                                        j+=1
                                        cellNum += 1
                                        BTSWeb_Wait1
                    BTSWeb_Wait1
            i += 1
        driver.refresh()
        BTSWeb_Wait1
AddingBTS()