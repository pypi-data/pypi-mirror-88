import unittest
from unittest import mock

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row, gridplot
from bokeh.models import HoverTool, ColumnDataSource

import Fittness.calories_intake.visualization as vi

class TestVisualization(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.lst1 = [50.0,60.0,45.0,87.0,32.0,69.0,78.0]
        cls.lst2 = [47,40,45,45,36,20,54]
        cls.lst3 = [126,155,102,135,120,169,110]
        cls.lst4 = [1,2,3,4,5,6,7]
        cls.lst5 = [2127,1220,1101,2816,2612,1800,1998]
        print('setUpClass')
        
    def setUp(self):
        self.v1 = figure()
        self.v1.circle(self.lst4, self.lst1)
        self.v2 = figure()
        self.v2.triangle(self.lst4, self.lst2)
        self.v3 = figure()
        self.v3.square(self.lst4, self.lst3)
        self.v4 = gridplot([[self.v1, self.v2, self.v3]])
        
        self.v5 = ColumnDataSource(data=dict(x = self.lst4, y = self.lst5))
        self.v6 = HoverTool(tooltips=[('index', '$index'), ('y', '@y')])
        self.v7 = figure(tools=[self.v6])
        self.v7.line('x', 'y', source=self.v5)
        self.v7.circle('x', 'y', source=self.v5)
        
    def test_type(self):
        self.assertEqual(str(type(self.v1)), "<class 'bokeh.plotting.figure.Figure'>")
        self.assertEqual(str(type(self.v2)), "<class 'bokeh.plotting.figure.Figure'>")
        self.assertEqual(str(type(self.v3)), "<class 'bokeh.plotting.figure.Figure'>")
        self.assertEqual(str(type(self.v4)), "<class 'bokeh.models.layouts.Column'>")
        self.assertEqual(str(type(self.v5)), "<class 'bokeh.models.sources.ColumnDataSource'>")
        self.assertEqual(str(type(self.v6)), "<class 'bokeh.models.tools.HoverTool'>")
        self.assertEqual(str(type(self.v7)), "<class 'bokeh.plotting.figure.Figure'>")
       
    
    @mock.patch('Fittness.calories_intake.visualization.input', create=True)
    def test_entry(self, mocked_input):
        mocked_input.side_effect = ['50 60 45 87 32 69 78', '47 40 45 45 36 20 54', '126 155 102 135 120 169 110']
        self.assertEqual(vi.entry(), [1127.0, 1220.0, 993.0, 1293.0, 932.0, 1132.0, 1238.0])
        
        mocked_input.side_effect = ['97 63 102 90 65 100 89 87', '69 65 80 97 67 54 80 63', '160 121 158 162 167 160 110 170']
        self.assertEqual(vi.entry(), [1649.0, 1321.0, 1760.0, 1881.0, 1531.0, 1526.0, 1516.0, 1595.0])
        
        mocked_input.side_effect = ['50 60 45 87 69 78', '47 40 45 45 36 20 54', '126 155 102 135 120 169 110']
        with self.assertRaises(ValueError) as context:
            vi.entry()
            
        self.assertEqual('We need records for at least a week', str(context.exception))
        
        mocked_input.side_effect = ['50 60 45 87 32 69 78', '47 40 45 45 36 20 54 98', '126 155 102 135 120 169 110']
        with self.assertRaises(ValueError) as context:
            vi.entry()
            
        self.assertEqual('Number of records for all 3 nutrients need to be the same', str(context.exception))

    
    def tearDown(self):
        self.v1 = None
        self.v2 = None
        self.v3 = None
        self.v4 = None
        self.v5 = None
        self.v6 = None
        self.v7 = None

    @classmethod
    def tearDownClass(cls):
        cls.lst1 = None
        cls.lst2 = None
        cls.lst3 = None
        cls.lst4 = None
        cls.lst5 = None
        print('tearDownClass')

unittest.main(argv=[''], verbosity=2, exit=False)