import unittest
from vscrap._scrap import _m_address, _extract_details, _retrieve_extension_page


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.address = "https://marketplace.visualstudio.com/items?itemName="

    def test_m_address(self):
        ins = ['MS-vsliveshare.vsls-vs', 'MadsKristensen.AddNewFile', 'wix.vscode-import-cost', 'namedfe']
        for _id in ins[:3]:
            self.assertEqual(f'{self.address}{_id}', _m_address(_id))

        self.assertRaises(ValueError, _m_address, ins[-1])

    def test_extract_details(self):
        texts = []
        exp_res = [
            {
                'title': 'Add New File',
                'publisher_name': 'Mads Kristensen',
                'default_image': 'https://madskristensen.gallerycdn.vsassets.io/extensions/madskristensen/'
                                 'addnewfile/3.5.150/1602087429945/Microsoft.VisualStudio.Services.Icons.Default',
                'installs': 464290
            },
            {
                'title': 'Live Share',
                'publisher_name': 'Microsoft',
                'default_image': 'https://ms-vsliveshare.gallerycdn.vsassets.io/extensions/ms-vsliveshare/vsls-vs/'
                                 '1.0.3121.0/1604534068310/Microsoft.VisualStudio.Services.Icons.Default',
                'installs': 251316
            },
            {
                'title': 'Visual Studio IntelliCode',
                'publisher_name': 'Microsoft',
                'default_image': 'https://visualstudioexptteam.gallerycdn.vsassets.io/extensions/'
                                 'visualstudioexptteam/vscodeintellicode/1.2.10/1597190336810/'
                                 'Microsoft.VisualStudio.Services.Icons.Default',
                'installs': 8412523
            },
            {
                'title': 'Import Cost',
                'publisher_name': 'Wix',
                'default_image': 'https://wix.gallerycdn.vsassets.io/extensions/wix/vscode-import-cost/'
                                 '2.13.0/1606917648353/Microsoft.VisualStudio.Services.Icons.Default',
                'installs': 852932
            },
        ]
        # load mock extensions text
        with open('examples.txt') as ex_f:
            for line in ex_f.readlines():
                texts.append(line)

        for text, res in zip(texts, exp_res):
            self.assertDictEqual(res, _extract_details(text))

    def test_retrieve_extension_page(self):
        urls = ['https://www.google.com/', 'https://www.google.com/search?q=home']
        self.assertEqual(str, type(_retrieve_extension_page(urls[0])))
        self.assertEqual(None, _retrieve_extension_page(urls[-1]))


if __name__ == '__main__':
    unittest.main()
