define([
    'nbextensions/visualpython/src/common/constant'
], function (vpConst) {
    // TEST
    // pandas 함수 설정값
    /**
     * Replaced with
    '([a-zA-Z0-9_.]*)'[ ]*: (\{[\n\t ]*id:)[ ]*'([a-zA-Z0-9]*)'
    '$3': $2 '$1'
    */
    var _PANDAS_FUNCTION = {
        'pd001': {
            id: 'Series',
            name: 'Series 생성',
            library: 'pandas',
            description: '동일한 데이터 타입의 1차원 배열 생성',
            code: '${o0} = pd.Series(${i0}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:['var', 'list', 'dict'],
                    label: 'data'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable',
                    component: 'input_single'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'index',
                    type:'list',
                    label: 'index'
                },
                {
                    index: 1,
                    name:'name',
                    type:'text',
                    label:'Series name'
                }
            ]
        },
        'pd002': {
            id: 'Dataframe',
            name: 'DataFrame 생성',
            library: 'pandas',
            description: '2차원의 Table 형태 변수 생성',
            code: '${o0} = pd.DataFrame(${i0}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:['var', 'list2d', 'dict'],
                    label: 'data',
                    component: 'table'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'index',
                    type:'list',
                    label:'index list'
                },
                {
                    index: 1,
                    name:'columns',
                    type:'list',
                    label:'column list'
                }
            ]
        },
        'pd003': {
            id: 'Index',
            name: 'Index 생성',
            library: 'pandas',
            description: '색인 객체 생성',
            code: '${o0} = pd.Index(${data}${v})',
            input: [
                {
                    index: 0,
                    name: 'data',
                    type: ['list', 'var'],
                    label: 'data'
                }
            ],
            variable: [
                {
                    index: 1,
                    name: 'dtype',
                    type: 'var',
                    label: 'numpy dtype',
                    component: 'option_select',
                    options: ["'object'", 'None', "'int32'", "'int64'", "'float32'", "'float64'", "'string'", "'complex64'", "'bool'"],
                    options_label: ['객체', '선택 안 함', '정수형(32)', '정수형(64)', '실수형(32)', '실수형(64)', '문자형', '복소수(64bit)', 'bool형'],
                    default: "'object'"
                },
                {
                    index: 2,
                    name: 'copy',
                    type: 'bool',
                    label: 'copy',
                    component: 'bool_checkbox',
                    default: false
                },
                {
                    index: 3,
                    name: 'name',
                    type: 'var',
                    label: 'index name'
                },
                {
                    index: 4,
                    name: 'tupleize_cols',
                    type: 'bool',
                    label: 'create MultiIndex',
                    default: true,
                    component: 'bool_checkbox'
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]

        },
        'pd004': {
            id: 'read_csv',
            name: 'Read CSV',
            library: 'pandas',
            description: '파일의 데이터를 읽어 DataFrame으로 생성',
            code: '${o0} = pd.read_csv(${i0}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'text',
                    label: 'file path',
                    component: 'file'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'names',
                    type:'list',
                    label: 'columns'
                },
                {
                    index: 1,
                    name:'usecols',
                    type: 'list',
                    label: 'column list to use'
                },
                {
                    index: 2,
                    name:'index_col',
                    type:'text',
                    label: 'column to use as index'
                },
                {
                    index: 2,
                    name:'na_values',
                    type:'list',
                    label: 'na values'
                },
                {
                    index: 3,
                    name:'header',
                    type:'int',
                    label: 'header index'
                },
                {
                    index: 4,
                    name: 'sep',
                    type: 'text',
                    label: 'seperator'
                },
                {
                    index: 5,
                    name: 'skiprows',
                    type: 'list',
                    label: 'rows to skip'
                },
                {
                    index: 6,
                    name: 'chunksize',
                    type: 'int',
                    label: 'chunksize'
                }
            ]
        },
        'pd005': {
            id: 'to_csv',
            name: 'To CSV',
            library: 'pandas',
            description: 'DataFrame을 csv 파일로 작성',
            code: '${i0}.to_csv(${i1}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name:'i1',
                    type:'text',
                    label: 'file path',
                    component: 'file'
                }
            ],
            output: [
            ],
            variable: [
                {
                    index: 0,
                    name:'header',
                    type:['bool', 'list'],
                    label: 'header index',
                    default: 'True'
                },
                {
                    index: 1,
                    name: 'index',
                    type: 'bool',
                    label: 'show index',
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 2,
                    name: 'sep',
                    type: 'text',
                    label: 'seperator'
                },
                {
                    index: 3,
                    name: 'na_rep',
                    type: 'text',
                    label: 'na replacing value'
                },
                {
                    index: 4,
                    name: 'columns',
                    type: 'list',
                    label: 'columns'
                }
            ]
        },
        'pd006': {
            id: 'select_row',
            name: '행 선택',
            library: 'pandas',
            description: '행 선택해 조회',
            code: '${o0} = ${i0}[${i1}:${i2}]',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name:'i1',
                    type:'int',
                    label: 'start row',
                    required: false
                },
                {
                    index: 2,
                    name:'i2',
                    type:'int',
                    label: 'end row',
                    required: false
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                },
            ],
            variable: [
            ]
        },
        'pd007': {
            id: 'select_column',
            name: '열 선택',
            library: 'pandas',
            description: '열 선택해 조회',
            code: '${o0} = ${i0}[${i1}]',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    var_type: ['DataFrame', 'Series'],
                    component: 'var_select'
                },
                {
                    index: 1,
                    name:'i1',
                    type:'list',
                    label: 'columns',
                    required: false
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                },
            ],
            variable: [
            ]
        },
        'pd008': {
            id: 'merge',
            name: 'Merge',
            library: 'pandas',
            description: '두 객체를 병합',
            code: '${o0} = pd.merge(${i0}, ${i1}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'left DataFrame',
                    component: 'var_select',
                    var_type: ['DataFrame']
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: 'right DataFrame',
                    component: 'var_select',
                    var_type: ['DataFrame']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'left_on',
                    type:'text',
                    label: 'left key'
                },
                {
                    index: 1,
                    name:'right_on',
                    type:'text',
                    label: 'right key'
                },
                {
                    index: 2,
                    name:'how',
                    type:'text',
                    label: 'merge type',
                    component: 'option_select',
                    options: ['left', 'right', 'inner', 'outer']
                },
                {
                    index: 3,
                    name:'sort',
                    type:'bool',
                    label: 'sort'
                }
            ]
        },
        'pd009': {
            id: 'join',
            name: 'Join',
            library: 'pandas',
            description: '다수의 객체를 병합',
            code: '${o0} = ${i0}.join(${i1}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: 'DataFrame to join',
                    component: 'var_select',
                    var_type: ['DataFrame']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'on',
                    type:'text',
                    label: 'key'
                },
                {
                    index: 1,
                    name:'how',
                    type:'text',
                    label: 'type',
                    component: 'option_select',
                    options: ['left', 'right', 'inner', 'outer']
                },
                {
                    index: 2,
                    name:'sort',
                    type:'bool',
                    label: 'sort',
                    component: 'bool_checkbox'
                },
                {
                    index: 3,
                    name:'lsuffix',
                    type:'text',
                    label: 'left suffix'
                },
                {
                    index: 4,
                    name:'rsuffix',
                    type:'text',
                    label: 'right suffix'
                }
            ]
        },
        'pd010': {
            id: 'concat',
            name: 'Concat',
            library: 'pandas',
            description: '다수의 객체를 병합',
            code: '${o0} = pd.concat(${i0}${v})',
            guide: [
                's1 = pd.Series([0, 1],    index=["a", "b"])',
                's2 = pd.Series([2, 3, 4], index=["c", "d", "e"])',
                '_concat = pd.concat([s1, s2], keys=["one", "two"], axis=1, sort=False, join="outer")',
                '_concat'
            ],
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'list',
                    label: 'target variable',
                    component: 'var_multi',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'index',
                    type:'list',
                    label:'index list'
                },
                {
                    index: 1,
                    name:'axis',
                    type:'int',
                    label:'axis',
                    help:'0:row / 1:column',
                    options:[0, 1],
                    options_label:['row', 'column'],
                    component:'option_select'
                },
                {
                    index: 2,
                    name:'sort',
                    type:'bool',
                    label:'sort',
                    component: 'bool_checkbox'
                },
                {
                    index: 3,
                    name:'join',
                    type:'text',
                    label:'join',
                    options: ['inner', 'outer'],
                    component: 'option_select'
                }
            ]
        },
        'pd011': {
            id: 'sort_index',
            name: 'Sort By Index',
            library: 'pandas',
            description: 'DataFrame/Series 객체를 index 기준으로 정렬',
            code: '${o0} = ${i0}.sort_index(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'axis',
                    type:'int',
                    label: 'sort by',
                    help: '0:row / 1:column',
                    component: 'option_select',
                    default: 0,
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name:'ascending',
                    type:'bool',
                    label: 'ascending sort',
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 2,
                    name:'inplace',
                    type:'bool',
                    label: 'inplace',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 3,
                    name: 'kind',
                    type: 'text',
                    label: 'sort kind',
                    default: 'quicksort',
                    component: 'option_select',
                    options: ['quicksort', 'mergesort', 'heapsort'],
                    options_label: ['quicksort', 'mergesort', 'heapsort']
                }
            ]
        },
        'pd012': {
            id: 'groupby',
            name: 'Group By',
            library: 'pandas',
            description: 'DataFrame/Series 객체의 그룹화',
            code: '${o0} = ${i0}.groupby(${level}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name:'level',
                    type:['var', 'int', 'text'],
                    label: 'grouping column'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 1,
                    name:'axis',
                    type:'int',
                    label: 'axis',
                    help: '0:row / 1:column',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 2,
                    name:'sort',
                    type:'bool',
                    label:'sort',
                    component: 'bool_checkbox'
                }, 
                {
                    index: 3,
                    name: 'as_index',
                    type: 'bool',
                    label: 'remove index',
                    help: 'same as reset_index()',
                    component: 'bool_checkbox',
                    default: true
                }
            ]
        },
        'pd013': {
            id: 'period',
            name: 'Period',
            library: 'pandas',
            description: 'Period 객체 생성',
            code: '${o0} = pd.Period(${i0}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:['int', 'text'],
                    label: 'date'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'freq',
                    label: 'frequency',
                    type: 'var',
                    component: 'option_select',
                    options: ['s', 'T', 'H', 'D', 'B', 'W', 'W-MON', 'M'],
                    options_label: ['초', '분', '시간', '일', '주말이 아닌 평일', '주(일요일)', '주(월요일)', '각 달의 마지막 날']
                },
                {
                    index : 1,
                    name: 'year',
                    type: 'int',
                    label: 'year'
                },
                {
                    index : 2,
                    name: 'month',
                    type: 'int',
                    label: 'month'                
                },
                {
                    index : 3,
                    name: 'day',
                    type: 'int',
                    label: 'day'
                }
            ]
        },
        'pd014': {
            id: 'dropna',
            name: 'Drop NA',
            library: 'pandas',
            description: 'dropna()로 결측치 처리',
            code: '${o0} = ${i0}.dropna(${v})',
            guide: [
                'from numpy import nan as NA',
                'data = Series([1, NA, 3.5, NA, 7])',
                'cleaned = data.dropna()'
            ],
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type:'int',
                    label: 'axis',
                    help: '0:row / 1:column',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'how',
                    type: 'text',
                    label: 'how',
                    help: 'any: drop if na exist more than one\nall: drop if na exist every row/column',
                    component: 'option_select',
                    options: ['any', 'all']
                },
                {
                    index: 2,
                    name: 'thresh',
                    type: 'int',
                    label: 'na minimum standard',
                    help: '결측치가 몇 개일 때 부터 제거할지 개수 입력'
                }
            ]
        },
        'pd015': {
            id: 'fillna',
            name: 'Fill NA',
            library: 'pandas',
            description: 'fillna()로 널 값 대체',
            code: '${o0} = ${i0}.fillna(${v})',
            guide: [
                'from numpy import nan as NA',
                'df = pd.DataFrame([[1,2,3,NA],[4,NA,1,2],[0,9,6,7]])',
                '# dictionary 형식으로 받았는데 앞의 key가 컬럼을 나타낸다',
                'df.fillna({1: 0.5, 3: -1})',
                '# fillna는 값을 채워 넣은 객체의 참조를 반환한다',
                '_ = df.fillna(0, inplace=True)'
            ],
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'value',
                    type: ['var', 'int', 'dict'],
                    label: 'value to fill'
                },
                {
                    index: 1,
                    name: 'axis',
                    type:'int',
                    label: 'axis',
                    help: '0:row / 1:column',
                    component: 'option_select',
                    default: 0,
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 2,
                    name: 'method',
                    type: 'var',
                    label: 'how',
                    help: 'ffill:fill with before value\nbfill:fill with after value',
                    component: 'option_select',
                    default: 'None',
                    options: ['None', "'ffill'", "'bfill'"],
                    options_label: ['선택 안 함', '이전 값으로 채우기', '이후 값으로 채우기']
                },
                {
                    index: 3,
                    name: 'inplace',
                    type: 'bool',
                    label: 'inplace',
                    component: 'bool_checkbox'
                },
                {
                    index: 4,
                    name: 'limit',
                    type: 'int',
                    label: 'gap limit',
                    help: '전/후 보간 시에 사용할 최대 갭 크기'

                }
            ]
        },
        'pd016': {
            id: 'duplicated',
            name: 'Get Duplicates',
            library: 'pandas',
            description: '중복 조회',
            code: '${o0} = ${i0}.duplicated(${v})',
            guide: [
                'data.duplicated()'
            ],
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'keep',
                    type:'var',
                    label: 'mark duplicated when',
                    help: 'first:첫 번째 항목 뺀 모두 중복으로 표시 / last:마지막 항목 뺀 모두 중복으로 표시 / False:모두 중복으로 표시',
                    component: 'option_select',
                    default: "'first'",
                    options: ["'first'", "'last'", 'False'],
                    options_label: ['첫 번째 항목 제외한 모두 중복으로 표시', '마지막 항목 제외한 모두 중복으로 표시', '모두 중복으로 표시']
                }
            ]
        },
        'pd017': {
            id: 'drop_duplicates',
            name: 'Drop  Duplicates',
            library: 'pandas',
            description: '중복된 항목 제거',
            code: '${o0} = ${i0}.drop_duplicates(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'keep',
                    type:'var',
                    label: 'mark duplicated when',
                    help: 'first:첫 번째 항목 뺀 모두 중복으로 표시 / last:마지막 항목 뺀 모두 중복으로 표시 / False:모두 중복으로 표시',
                    component: 'option_select',
                    default: "'first'",
                    options: ["'first'", "'last'", 'False'],
                    options_label: ['첫 번째 항목 제외한 모두 중복으로 표시', '마지막 항목 제외한 모두 중복으로 표시', '모두 중복으로 표시']
                }
            ]
        },
        'pd018': {
            id: 'replace_scala',
            name: 'Scala Replace',
            library: 'pandas',
            description: 'Scala 값 치환',
            code: '${o0} = ${i0}.replace(${v})',
            guide: [
                `s = pd.Series([0, 1, 2, 3, 4])`,
                `s.replace(0, 5)`,
                `df = pd.DataFrame({'A': [0, 1, 2, 3, 4],`,
                `                   'B': [5, 6, 7, 8, 9],`,
                `                   'C': ['a', 'b', 'c', 'd', 'e']})`,
                `df.replace(0, 5)`
            ],
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'to_replace',
                    type:'int',
                    label: 'to replace',
                    required: true
                },
                {
                    index: 1,
                    name:'value',
                    type:'int',
                    label: 'replace value',
                },
                {
                    index: 2,
                    name: 'method',
                    type:'var',
                    label: 'method',
                    options: ["'ffill'", "'bfill'", 'None'],
                    options_label: ['이전 값으로 채우기', '이후 값으로 채우기', '선택 안 함'],
                    component: 'option_select',
                    default: "'ffill'"
                }
            ]
        },
        'pd019': {
            id: 'replace_list',
            name: 'List-like Replace',
            library: 'pandas',
            description: 'List 값 치환',
            code: '${o0} = ${i0}.replace(${v})',
            guide: [
                `df.replace([0, 1, 2, 3], 4)`,
                `df.replace([0, 1, 2, 3], [4, 3, 2, 1])`,
                `s.replace([1, 2], method='bfill')`
            ],
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'to_replace',
                    type:'list',
                    label: 'to replace',
                    required: true
                },
                {
                    index: 1,
                    name:'value',
                    type:['int', 'list'],
                    label: 'value',
                },
                {
                    index: 2,
                    name: 'method',
                    type:'var',
                    label: 'method',
                    options: ["'ffill'", "'bfill'", 'None'],
                    options_label: ['이전 값으로 채우기', '이후 값으로 채우기', '선택 안 함'],
                    component: 'option_select',
                    default: "'ffill'"
                }
            ]
        },
        'pd020': {
            id: 'replace_dict',
            name: 'Dict-like Replace',
            library: 'pandas',
            description: 'Dictionary 값 치환',
            code: '${o0} = ${i0}.replace(${v})',
            guide: [
                `df.replace({0: 10, 1: 100})`,
                `df.replace({'A': 0, 'B': 5}, 100)`,
                `df.replace({'A': {0: 100, 4: 400}})`
            ],
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'to_replace',
                    type:'dict',
                    label: 'to replace',
                    required: true
                },
                {
                    index: 1,
                    name:'value',
                    type:['int', 'dict'],
                    label: 'value',
                },
                {
                    index: 2,
                    name: 'method',
                    type:'var',
                    label: 'method',
                    options: ["'ffill'", "'bfill'", 'None'],
                    options_label: ['이전 값으로 채우기', '이후 값으로 채우기', '선택 안 함'],
                    component: 'option_select',
                    default: "'ffill'"
                }
            ]
        },
        // TODO: 정규식은 PENDING
        'pd021': {
            id: 'replace_regex',
            name: 'Regular Expression Replace',
            library: 'pandas',
            description: '정규식 치환',
            code: '${o0} = ${i0}.replace(${v})',
            guide: [
                `df = pd.DataFrame({'A': ['bat', 'foo', 'bait'],`,
                `                   'B': ['abc', 'bar', 'xyz']})`,
                `df.replace(to_replace=r'^ba.$', value='new', regex=True)`,
                `df.replace({'A': r'^ba.$'}, {'A': 'new'}, regex=True)`,
                `df.replace(regex=r'^ba.$', value='new')`,
                `df.replace(regex={r'^ba.$': 'new', 'foo': 'xyz'})`,
                `df.replace(regex=[r'^ba.$', 'foo'], value='new')`
            ],
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'to_replace',
                    type:'dict',
                    label: '바꿀 값',
                    required: true
                },
                {
                    index: 1,
                    name:'value',
                    type:['text', 'dict'],
                    label: '바뀔 값',
                },
                {
                    index: 2,
                    name: 'method',
                    type:'var',
                    label: '치환 방식',
                    options: ["'ffill'", "'bfill'", 'None'],
                    options_label: ['이전 값으로 채우기', '이후 값으로 채우기', '선택 안 함'],
                    component: 'option_select',
                    default: "'ffill'"
                },
                {
                    index: 3,
                    name: 'regex',
                    type:'bool',
                    label:'정규식',
                    options: [true, false]
                }
            ]
        },
        'pd022': {
            id: 'sum',
            name: 'Sum',
            library: 'pandas',
            description: '합계 계산',
            code: '${o0} = ${i0}.sum(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    description: '연산을 수행할 축. DataFrame에서 0은 로우고 1은 칼럼이다.',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'skipna',
                    type: 'bool',
                    label: '결측치 제외',
                    description: '누락된 값을 제외할 것인지 정하는 옵션. 기본값은 True다.',
                    component: 'bool_checkbox',
                    default: true
                },
                {
                    index: 2,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '레벨',
                    description: '계산하려는 축이 계층적 색인(다중 색인)이라면 레벨에 따라 묶어서 계산한다.'
                }
            ]
        },
        'pd023': {
            id: 'mean',
            name: 'Mean',
            library: 'pandas',
            description: '평균 계산',
            code: '${o0} = ${i0}.mean(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    description: '연산을 수행할 축. DataFrame에서 0은 로우고 1은 칼럼이다.',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'skipna',
                    type: 'bool',
                    label: '결측치 제외',
                    description: '누락된 값을 제외할 것인지 정하는 옵션. 기본값은 True다.',
                    component: 'bool_checkbox',
                    default: true
                },
                {
                    index: 2,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '레벨',
                    description: '계산하려는 축이 계층적 색인(다중 색인)이라면 레벨에 따라 묶어서 계산한다.'
                }
            ]
        },
        'pd024': {
            id: 'count',
            name: 'Count',
            library: 'pandas',
            description: 'NA 값을 제외한 값의 수를 계산',
            code: '${o0} = ${i0}.count(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    description: '연산을 수행할 축. DataFrame에서 0은 로우고 1은 칼럼이다.',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'skipna',
                    type: 'bool',
                    label: '결측치 제외',
                    description: '누락된 값을 제외할 것인지 정하는 옵션. 기본값은 True다.',
                    component: 'bool_checkbox',
                    default: true
                },
                {
                    index: 2,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '레벨',
                    description: '계산하려는 축이 계층적 색인(다중 색인)이라면 레벨에 따라 묶어서 계산한다.'
                }
            ]
        },
        'pd025': {
            id: 'max',
            name: 'Max',
            library: 'pandas',
            description: '최대값을 계산',
            code: '${o0} = ${i0}.max(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    description: '연산을 수행할 축. DataFrame에서 0은 로우고 1은 칼럼이다.',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'skipna',
                    type: 'bool',
                    label: '결측치 제외',
                    description: '누락된 값을 제외할 것인지 정하는 옵션. 기본값은 True다.',
                    component: 'bool_checkbox',
                    default: true
                },
                {
                    index: 2,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '레벨',
                    description: '계산하려는 축이 계층적 색인(다중 색인)이라면 레벨에 따라 묶어서 계산한다.'
                }
            ]
        },
        'pd026': {
            id: 'min',
            name: 'Min',
            library: 'pandas',
            description: '최소값을 계산',
            code: '${o0} = ${i0}.min(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    description: '연산을 수행할 축. DataFrame에서 0은 로우고 1은 칼럼이다.',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'skipna',
                    type: 'bool',
                    label: '결측치 제외',
                    description: '누락된 값을 제외할 것인지 정하는 옵션. 기본값은 True다.',
                    component: 'bool_checkbox',
                    default: true
                },
                {
                    index: 2,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '레벨',
                    description: '계산하려는 축이 계층적 색인(다중 색인)이라면 레벨에 따라 묶어서 계산한다.'
                }
            ]
        },
        'pd027': {
            id: 'median',
            name: 'Median',
            library: 'pandas',
            description: '중간값(50% 분위)을 계산',
            code: '${o0} = ${i0}.median(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    description: '연산을 수행할 축. DataFrame에서 0은 로우고 1은 칼럼이다.',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'skipna',
                    type: 'bool',
                    label: '결측치 제외',
                    description: '누락된 값을 제외할 것인지 정하는 옵션. 기본값은 True다.',
                    component: 'bool_checkbox',
                    default: true

                },
                {
                    index: 2,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '레벨',
                    description: '계산하려는 축이 계층적 색인(다중 색인)이라면 레벨에 따라 묶어서 계산한다.'
                },
                {
                    index: 3,
                    name: 'numeric_only',
                    label: '숫자만 집계',
                    var_type: ['DataFrame'],
                    type: 'var',
                    component: 'option_select',
                    default: 'None',
                    options: ['None', "'false'", "'true'"],
                    options_label: ['선택 안 함', '모두 집계', '숫자만 집계']
                }
            ]
        },
        'pd028': {
            id: 'std',
            name: 'Std',
            library: 'pandas',
            description: '표본 정규 분산의 값을 계산',
            code: '${o0} = ${i0}.std(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    description: '연산을 수행할 축. DataFrame에서 0은 로우고 1은 칼럼이다.',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'skipna',
                    type: 'bool',
                    label: '결측치 제외',
                    description: '누락된 값을 제외할 것인지 정하는 옵션. 기본값은 True다.',
                    component: 'bool_checkbox',
                    default: true
                },
                {
                    index: 2,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '레벨',
                    description: '계산하려는 축이 계층적 색인(다중 색인)이라면 레벨에 따라 묶어서 계산한다.'
                },
                {
                    index: 3,
                    name: 'numeric_only',
                    label: '숫자만 집계',
                    var_type: ['DataFrame'],
                    type: 'var',
                    component: 'option_select',
                    default: 'None',
                    options: ['None', "'false'", "'true'"],
                    options_label: ['선택 안 함', '모두 집계', '숫자만 집계']
                }
            ]
        },
        'pd029': {
            id: 'quantile',
            name: 'Quantile',
            library: 'pandas',
            description: '0부터 1까지의 분위수를 계산',
            code: '${o0} = ${i0}.quantile(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'q',
                    type: ['float', 'list'],
                    label: '백분위수(0~1사이 값)',
                    description: '',
                    default: 0.5
                },
                {
                    index: 1,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    description: '연산을 수행할 축. DataFrame에서 0은 로우고 1은 칼럼이다.',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 2,
                    name: 'numeric_only',
                    label: '숫자만 집계',
                    var_type: ['DataFrame'],
                    type: 'var',
                    component: 'option_select',
                    options: ['False', 'True'],
                    options_label: ['모두 집계', '숫자만 집계']
                },
                {
                    index: 3,
                    name: 'interpolation',
                    label: 'interpolation',
                    type: 'text',
                    component: 'option_select',
                    options: ['linear','lower', 'higher', 'nearest', 'midpoint'],
                    default: 'linear'
                }
            ]
        },
        'pd030': {
            id: 'drop',
            name: 'Drop Row/Column',
            library: 'pandas',
            description: '지정한 행/열을 삭제',
            code: '${o0} = ${i0}.drop(${i1}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name:'i1',
                    type: ['var', 'int', 'text'],
                    label: '행/열 인덱스',
                    // component: 'var_select',
                    var_type: ['column', 'index'],
                    var_para: ['i0']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'axis',
                    type:'int',
                    label:'행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                }
            ]
        },
        'pd031': {
            id: 'date_range',
            name: 'date_range',
            library: 'pandas',
            description: '정규 날짜 시퀀스를 DatetimeIndex형 타임스탬프로 생성',
            code: '${o0} = pd.date_range(${v})',
            input: [
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'start',
                    label: '시작일',
                    help: 'yyyy-MM-dd 의 형식으로 날짜를 작성한다',
                    type: 'text'
                },
                {
                    index: 1,
                    name: 'end',
                    label: '종료일',
                    help: 'yyyy-MM-dd 의 형식으로 날짜를 작성한다',
                    type: 'text'
                },
                {
                    index: 2,
                    name: 'periods',
                    type: 'int',
                    label: '생성할 인덱스 개수',
                    help: '생성할 날짜 인덱스의 개수를 입력한다'
                },
                {
                    index: 3,
                    name: 'freq',
                    label: '주기',
                    type: 'text',
                    component: 'option_select',
                    options: ['s', 'T', 'H', 'D', 'B', 'W', 'W-MON', 'MS', 'M', 'BMS', 'BM'],
                    options_label: ['초', '분', '시간', '일', '주말이 아닌 평일', '주(일요일)', '주(월요일)', '각 달의 첫날', '각 달의 마지막 날', '평일 중 각 달의 첫날', '평일 중 각 달의 마지막 날']
                }
            ]
        },
        'pd032': {
            id: 'sort_values',
            name: 'Sort By Values',
            library: 'pandas',
            description: 'Series/DataFrame의 데이터를 기준으로 정렬',
            code: '${o0} = ${i0}.sort_values(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'by',
                    type: ['list', 'text'],
                    label: '정렬 기준 행/열 이름',
                    required: true
                },
                {
                    index: 1,
                    name:'axis',
                    type:'int',
                    label: '정렬 대상',
                    help: '0:행 / 1:열',
                    component: 'option_select',
                    default: 0,
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 2,
                    name:'ascending',
                    type:'bool',
                    label: '오름차순 정렬',
                    component: 'bool_checkbox',
                    default: true
                },
                {
                    index: 3,
                    name:'inplace',
                    type:'bool',
                    label: '바로 적용',
                    component: 'bool_checkbox',
                    default: false
                },
                {
                    index: 4,
                    name: 'kind',
                    type: 'text',
                    label: '정렬 유형',
                    component: 'option_select',
                    default: 'quicksort',
                    options: ['quicksort', 'mergesort', 'heapsort'],
                    options_label: ['퀵정렬', '합병정렬', '힙정렬']
                }
            ]
        },
        'pd033': {
            id: 'isnull',
            name: 'Is Null',
            library: 'pandas',
            description: 'Series/DataFrame의 결측치 탐색',
            code: '${o0} = pd.isnull(${i0})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable',
                    help: '결측치 여부를 마스킹한 DataFrame/Series'
                }
            ],
            variable: [
            ]
        },
        'pd034': {
            id: 'notnull',
            name: 'Not Null',
            library: 'pandas',
            description: 'Series/DataFrame의 결측치가 아닌 값을 탐색',
            code: '${o0} = pd.notnull(${i0})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable',
                    help: '결측치가 아닌 값을 마스킹한 DataFrame/Series'
                }
            ],
            variable: [
            ]
        },
        'pd035': {
            id: '.T',
            name: 'Transpose',
            library: 'pandas',
            description: '행/열을 바꿔 조회',
            code: '${o0} = ${i0}.T',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Index']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd036': {
            id: '.columns',
            name: 'Columns 조회',
            library: 'pandas',
            description: '열 목록 조회',
            code: '${o0} = ${i0}.columns',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd037': {
            id: '.index',
            name: 'index 조회',
            library: 'pandas',
            description: '행 목록 조회',
            code: '${o0} = ${i0}.index',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd038': {
            id: '.values',
            name: 'Values 조회',
            library: 'pandas',
            description: '내부 값들만 조회',
            code: '${o0} = ${i0}.values',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Index']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd039': {
            id: '.name',
            name: 'name 조회',
            library: 'pandas',
            description: '객체의 이름 조회',
            code: '${o0} = ${i0}.name',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd040': {
            id: 'loc',
            name: 'Loc',
            library: 'pandas',
            description: 'index 이름으로 행 선택',
            code: '${o0} = ${i0}.loc[${i1}]',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name: 'i1',
                    type: ['text', 'list'],
                    label: 'row/column name to find'
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd041': {
            id: 'iloc',
            name: 'iLoc',
            library: 'pandas',
            description: 'index 위치로 행 선택',
            code: '${o0} = ${i0}.iloc[${i1}]',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name: 'i1',
                    type: ['text', 'list'],
                    label: 'row/column to count'
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd042': {
            id: '.array',
            name: 'array 조회',
            library: 'pandas',
            description: '객체의 배열 조회',
            code: '${o0} = ${i0}.array',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series', 'Index']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd043': {
            id: '.axes',
            name: 'axes 조회',
            library: 'pandas',
            description: 'Series의 인덱스 조회',
            code: '${o0} = ${i0}.axes',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd044': {
            id: '.hasnans',
            name: 'hasnans 조회',
            library: 'pandas',
            description: 'NAN 값을 갖고 있는지 여부를 확인',
            code: '${o0} = ${i0}.hasnans',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series', 'Index']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd045': {
            id: '.shape',
            name: 'shape 조회',
            library: 'pandas',
            description: '객체의 행/열 크기를 튜플 형태로 반환',
            code: '${o0} = ${i0}.shape',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series', 'Index']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd046': {
            id: '.dtype',
            name: 'dtype 조회',
            library: 'pandas',
            description: 'Index 객체의 데이터타입 조회',
            code: '${o0} = ${i0}.dtype',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Index']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd047': {
            id: 'len',
            name: '크기 조회',
            library: 'pandas',
            description: '배열 객체의 길이 조회',
            code: '${o0} = len(${i0})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Index']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd048': {
            id: 'unique',
            name: '고유값 조회',
            library: 'pandas',
            description: '객체의 고유값 목록을 조회',
            code: '${o0} = ${i0}.unique()',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series', 'Index']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd049': {
            id: 'value_counts',
            name: '데이터 개수 조회',
            library: 'pandas',
            description: '각 데이터별 개수 집계',
            code: '${o0} = ${i0}.value_counts()',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series', 'Index']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd050': {
            id: 'info',
            name: '기본 정보 조회',
            library: 'pandas',
            description: 'DataFrame 객체의 정보(컬럼별 정보, 데이터타입, 메모리 사용량 등) 조회',
            code: '${o0} = ${i0}.info()',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd051': {
            id: 'describe',
            name: '기본 상세정보 조회',
            library: 'pandas',
            description: 'DataFrame/Series 객체의 행/열별 집계 연산',
            code: '${o0} = ${i0}.describe()',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd052': {
            id: 'add',
            name: 'Add 산술연산',
            library: 'pandas',
            description: 'DataFrame/Series의 덧셈연산',
            code: '${o0} = ${i0}.add(${i1}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name:'i1',
                    type:['var', 'int'],
                    label: '더할 DataFrame/Series',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['행(index)', '열(columns)']
                },
                {
                    index: 1,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '연산 레벨'
                },
                {
                    index: 2,
                    name: 'fill_value',
                    type: 'float',
                    label: '결측치 대체값'
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd053': {
            id: 'sub',
            name: 'Sub 산술연산',
            library: 'pandas',
            description: 'DataFrame/Series의 뺄셈연산',
            code: '${o0} = ${i0}.sub(${i1}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name:'i1',
                    type:['var', 'int'],
                    label: '뺄 DataFrame/Series',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['행(index)', '열(columns)']
                },
                {
                    index: 1,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '연산 레벨'
                },
                {
                    index: 2,
                    name: 'fill_value',
                    type: 'float',
                    label: '결측치 대체값'
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd054': {
            id: 'div',
            name: 'Div 산술연산',
            library: 'pandas',
            description: 'DataFrame/Series의 나눗셈연산',
            code: '${o0} = ${i0}.div(${i1}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name:'i1',
                    type:['var', 'int'],
                    label: '나눌 DataFrame/Series',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['행(index)', '열(columns)']
                },
                {
                    index: 1,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '연산 레벨'
                },
                {
                    index: 2,
                    name: 'fill_value',
                    type: 'float',
                    label: '결측치 대체값'
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd055': {
            id: 'mul',
            name: 'Mul 산술연산',
            library: 'pandas',
            description: 'DataFrame/Series의 곱셈연산',
            code: '${o0} = ${i0}.mul(${i1}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name:'i1',
                    type:['var', 'int'],
                    label: '곱할 DataFrame/Series',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['행(index)', '열(columns)']
                },
                {
                    index: 1,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '연산 레벨'
                },
                {
                    index: 2,
                    name: 'fill_value',
                    type: 'float',
                    label: '결측치 대체값'
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd056': {
            id: 'insert_column',
            name: 'Insert Column',
            library: 'pandas',
            description: 'DataFrame의 열 추가',
            code: '${o0} = ${i0}.insert(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'loc',
                    type: 'int',
                    label: '추가할 열 위치',
                    required: true
                },
                {
                    index: 1,
                    name: 'column',
                    type: ['int', 'text', 'var', 'dict'],
                    label: '열 이름',
                    required: true
                },
                {
                    index: 2,
                    name: 'value',
                    type: ['int', 'var', 'list'],
                    label: '값',
                    required: true
                },
                {
                    index: 3,
                    name: 'allow_duplicates',
                    label: '중복 허용',
                    type: 'bool',
                    default: false,
                    component: 'bool_checkbox'
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd057': {
            id: 'insert_column_value',
            name: 'Insert Column Value',
            library: 'pandas',
            description: 'DataFrame의 열 추가',
            code: '${i0}[${i1}] = ${i2}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                },
                {
                    index: 1,
                    name:'i1',
                    type:'text',
                    label: '열 이름',
                    var_type: ['columns']
                },
                {
                    index: 2,
                    name:'i2',
                    type: ['var', 'int', 'text', 'list'],
                    label: '추가할 값'
                }
            ],
            variable: [],
            output: []
        },
        'pd058': {
            id: 'insert_row_loc',
            name: 'Insert Row Value',
            library: 'pandas',
            description: 'DataFrame의 행 추가',
            code: '${i0}.loc[${i1}] = ${i2}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                },
                {
                    index: 1,
                    name:'i1',
                    type:['int', 'text'],
                    label: '행 이름/위치',
                    var_type: ['index']
                },
                {
                    index: 2,
                    name:'i2',
                    type: ['var', 'int', 'text', 'list'],
                    label: '추가할 값'
                }
            ],
            variable: [],
            output: []
        },
        'pd059': {
            id: '.groups',
            name: 'Groups',
            library: 'pandas',
            description: 'GroupBy 객체의 groups 조회',
            code: '${o0} = ${i0}.groups',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: '대상 GroupBy 객체',
                    component: 'var_select',
                    var_type: ['GroupBy']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd060': {
            id: 'reindex',
            name: 'Reindex',
            library: 'pandas',
            description: 'DataFrame/Series/Index의 index를 수정',
            code: '${o0} = ${i0}.reindex(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Index']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'labels',
                    type: 'list',
                    label: '새 라벨'
                },
                {
                    index: 1,
                    name: 'index',
                    type: 'list',
                    label: '새 인덱스'
                },
                {
                    index: 2,
                    name: 'columns',
                    type: 'list',
                    label: '새 컬럼'
                },
                {
                    index: 3,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    component: 'option_select'
                },
                {
                    index: 4,
                    name: 'method',
                    type: 'text',
                    label: '채우기 방식',
                    help: 'ffill:이전 값으로 채우기\nbfill:뒤에 있는 값으로 채우기',
                    component: 'option_select',
                    options: ['ffill', 'bfill', 'nearest'],
                    options_label: ['이전 값으로 채우기', '이후 값으로 채우기', '가장 가까운 값으로 채우기']
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd061': {
            id: 'set_index',
            name: 'Set Index Values',
            library: 'pandas',
            description: 'DataFrame의 column을 이용해 index를 생성',
            code: '${o0} = ${i0}.set_index(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'keys',
                    type: ['text', 'list'],
                    label: '인덱스로 세팅할 열 이름',
                    required: true
                },
                {
                    index: 1,
                    name: 'drop',
                    type: 'bool',
                    label: '인덱스로 설정한 열 삭제 여부',
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 2,
                    name: 'append',
                    type: 'bool',
                    label: '기존에 존재하던 인덱스 삭제 여부',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 3,
                    name: 'inplace',
                    type: 'bool',
                    label: '바로 적용',
                    default: false,
                    component: 'bool_checkbox'
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd062': {
            id: 'reset_index',
            name: 'Reset Index Values',
            library: 'pandas',
            description: 'DataFrame/Series의 index를 이용해 column을 생성',
            code: '${o0} = ${i0}.reset_index(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'level',
                    type: ['int', 'text', 'list'],
                    label: '인덱스로 세팅할 열 이름',
                    default: 'None'
                },
                {
                    index: 1,
                    name: 'drop',
                    type: 'bool',
                    label: '인덱스로 설정한 열 삭제 여부',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 2,
                    name: 'inplace',
                    type: 'bool',
                    label: '바로 적용',
                    default: false,
                    component: 'bool_checkbox'
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type: 'var',
                    label: 'return variable'
                }
            ]
        },
        'pd063': {
            id: 'edit_row_data',
            name: 'Edit Row Data',
            library: 'pandas',
            description: 'DataFrame/Series/Index객체의 index 데이터 수정',
            code: '${i0}[${i1}] = ${i2}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name: 'i1',
                    type: 'var',
                    label: '행 이름/위치',
                },
                {
                    index: 2,
                    name: 'i2',
                    type: ['var', 'list', 'text', 'int'],
                    label: '수정할 값'
                }
            ],
            variable: [],
            output: []  
        },
        'pd064': {
            id: 'head',
            name: 'Head',
            library: 'pandas',
            description: '첫 n줄의 데이터 확인',
            code: '${o0} = ${i0}.head(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'n',
                    type: 'int',
                    label: 'count',
                    default: 5
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd065': {
            id: 'tail',
            name: 'Tail',
            library: 'pandas',
            description : '마지막 n줄의 데이터 확인',
            code: '${o0} = ${i0}.tail(${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'n',
                    type: 'int',
                    label: 'count',
                    default: 5
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd066': {
            id: 'take',
            name: 'Take',
            library: 'pandas',
            description: 'index로 데이터 조회',
            code: '${o0} = ${i0}.take(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Index']
                },
                {
                    index: 1,
                    name: 'i1',
                    type: 'list',
                    label: 'search index'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: '조회 기준',
                    options: [0, 1, 'None'],
                    options_label: ['행', '열', '선택 안 함'],
                    component: 'option_select',
                    default: 0
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd067': {
            id: 'op_add',
            name: '+',
            library: 'pandas',
            description: '변수 덧셈 연산',
            code: '${o0} = ${i0} + ${i1}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: '변수1'
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: '변수2'
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd068': {
            id: 'op_sub',
            name: '-',
            library: 'pandas',
            description: '변수 뺄셈 연산',
            code: '${o0} = ${i0} - ${i1}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: '변수1'
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: '변수2'
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd069': {
            id: 'op_mul',
            name: '*',
            library: 'pandas',
            description: '변수 곱셈 연산',
            code: '${o0} = ${i0} * ${i1}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: '변수1'
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: '변수2'
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd070': {
            id: 'op_pow',
            name: '**',
            library: 'pandas',
            description: '변수 n승 연산',
            code: '${o0} = ${i0} ** ${i1}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: '변수1'
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: '변수2'
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd071': {
            id: 'op_div',
            name: '/',
            library: 'pandas',
            description: '변수 나눗셈 연산',
            code: '${o0} = ${i0} / ${i1}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: '변수1'
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: '변수2'
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd072': {
            id: 'op_mod',
            name: '//',
            library: 'pandas',
            description: '변수 나눗셈(몫) 연산',
            code: '${o0} = ${i0} // ${i1}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: '변수1'
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: '변수2'
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd073': {
            id: 'op_mod_left',
            name: '%',
            library: 'pandas',
            description: '변수 나눗셈(나머지) 연산',
            code: '${o0} = ${i0} % ${i1}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: '변수1'
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: '변수2'
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd074': {
            id: 'bool',
            name: 'bool',
            library: 'pandas',
            description: 'bool형 연산',
            code: '${o0} = ${i0} ${i2} ${i1}',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: '변수1'
                },
                {
                    index: 1,
                    name:'i1',
                    type:'var',
                    label: '변수2'
                },
                {
                    index: 2,
                    name:'i2',
                    type:'var',
                    label: '연산자',
                    component: 'option_select',
                    options: ['==', '!=', '<', '<=', '>', '>=']
                }
            ],
            variable: [],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label: 'return variable'
                },
            ]
        },
        'pd075': {
            id: 'copy',
            name: 'copy',
            library: 'pandas',
            description: '데이터 복사',
            code: '${o0} = ${i0}.copy(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Index']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'deep',
                    type: 'bool',
                    label: '깊은 복사',
                    default: true,
                    component: 'bool_checkbox'
                }
            ],
            output: [
                {
                    index: 0,
                    name: 'o0',
                    type:'var',
                    label: 'return variable'
                }
            ]
        },
        'pd076': {
            id: 'read_json',
            name: 'Read Json',
            library: 'pandas',
            description: 'json형식 파일을 읽어 DataFrame/Series로 생성',
            code: '${o0} = pd.read_json(${i0}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'text',
                    label: 'file path',
                    component: 'file'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name:'typ',
                    type:'text',
                    label: '변환할 개체 유형',
                    component: 'option_select',
                    options: ['frame', 'series'],
                    default: 'frame'
                },
                {
                    index: 1,
                    name: 'orient',
                    type: 'text',
                    label: 'JSON 구조',
                    options: ['split', 'records', 'index', 'columns', 'values', 'table'],
                    default: 'columns' // typ=series일 경우, index가 default
                },
                {
                    index: 2,
                    name:'convert_dates',
                    type: 'list',
                    label: '날짜로 변환할 컬럼 목록'
                },
                {
                    index: 3,
                    name:'index_col',
                    type:'text',
                    label: '행 인덱스로 지정할 열'
                },
                {
                    index: 4,
                    name: 'encoding',
                    type: 'text',
                    label: '인코딩 방식',
                    default: 'utf-8'
                },
                {
                    index: 5,
                    name: 'chunksize',
                    type: 'int',
                    label: '순회할 데이터양'
                }
            ]
        },
        'pd077': {
            id: 'to_json',
            name: 'To Json',
            library: 'pandas',
            description: 'DataFrame/Series 데이터로 Json 파일 생성',
            code: '${o0} = ${i0}.to_json(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'path_or_buf',
                    type: 'text',
                    label: 'file path/variable'
                }, 
                {
                    index: 1,
                    name: 'orient',
                    type: 'text',
                    label: 'JSON 구조',
                    // options: series 객체일 경우 0~3 / dataframe 객체는 모두
                    options: ['split', 'records', 'index', 'table', 'columns', 'values']
                }
            ]
        },
        'pd078': {
            id: 'to_pickle',
            name: 'To Pickle',
            library: 'pandas',
            description: 'DataFrame/Series 데이터로 Pickle 파일 생성',
            code: '${i0}.to_pickle(${path})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name: 'path',
                    type: 'text',
                    label: 'file path/variable',
                    required: true
                }
            ],
            variable: [
                
            ]
        },
        'pd079': {
            id: 'read_pickle',
            name: 'Read Pickle',
            library: 'pandas',
            description: 'Pickle 파일에서 Pandas 객체 복구',
            code: '${o0} = pd.read_pickle(${i0}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type: 'text',
                    label: 'file path/object',
                    component: 'file'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
            ]
        },
        'pd080': {
            id: 'combine_first',
            name: 'Combine First',
            library: 'pandas',
            description: '참조 객체의 동일한 위치의 값을 결측치 대체값으로 사용',
            code: '${o0} = ${i0}.combine_first(${i1})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name: 'i1',
                    type:'var',
                    label: '참조할 DataFrame/Series',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [ ]
        },
        'pd081': {
            id: 'stack',
            name: 'Stack',
            library: 'pandas',
            description: 'DataFrame의 컬럼을 인덱스층에 추가',
            code: '${o0} = ${i0}.stack(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'level',
                    type: ['int', 'text', 'list'],
                    label: '컬럼 인덱스',
                    default: -1,
                },
                {
                    index: 1,
                    name: 'dropna',
                    type: 'bool',
                    label: '결측치 제거 여부',
                    default: true,
                    component: 'bool_checkbox'
                }
            ]
        },
        'pd082': {
            id: 'unstack',
            name: 'Unstack',
            library: 'pandas',
            description: '계층적 인덱스 중 특정계층의 index를 컬럼으로 변환',
            code: '${o0} = ${i0}.unstack(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'level',
                    type: ['int', 'text', 'list'],
                    label: '인덱스 계층 레벨',
                    default: -1,
                },
                {
                    index: 1,
                    name: 'fill_value',
                    type: ['int', 'text', 'var', 'dict'],
                    label: '결측치 대체값'
                }
            ]
        },
        'pd083': {
            id: 'pivot',
            name: 'Pivot',
            library: 'pandas',
            description: '행 데이터를 열 데이터로 회전해 데이터 재구조화',
            code: '${o0} = ${i0}.pivot(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'index',
                    type: ['text', 'var'],
                    label: 'index'
                },
                {
                    index: 1,
                    name: 'columns',
                    type: ['text', 'var'],
                    label: 'columns'
                },
                {
                    index: 2,
                    name: 'values',
                    type: ['text', 'var', 'list'],
                    label: 'value에 채우고자 하는 컬럼명/목록'
                }
            ]
        },
        'pd084': {
            id: 'melt',
            name: 'Melt',
            library: 'pandas',
            description: '특정컬럼과 데이터를 variable과 value 형태로 재구조화',
            code: '${o0} = ${i0}.melt(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'id_vars',
                    type: ['var', 'list'],
                    label: '식별키로 사용할 컬럼 목록'
                },
                {
                    index: 1,
                    name: 'value_vars',
                    type: ['var', 'list'],
                    label: '데이터 재구조화할 컬럼 목록'
                },
                {
                    index: 2,
                    name: 'var_name',
                    type: 'int',
                    label: 'variable 컬럼명'
                },
                {
                    index: 3,
                    name: 'value_name',
                    type: 'int',
                    label: 'value 컬럼명'
                },
                {
                    index: 4,
                    name: 'col_level',
                    type: ['int', 'text'],
                    label: '계층 인덱스 값'
                }
            ]
        },
        'pd085': {
            id: 'map',
            name: 'Map',
            library: 'pandas',
            description: '함수/매핑을 이용해 데이터 변형',
            code: '${o0} = ${i0}.map(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series', 'Index']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'arg',
                    type: ['var', 'dict'],
                    label: '매핑할 값/함수',
                    required: true
                },
                {
                    index: 1,
                    name: 'na_action',
                    type: 'var',
                    label: '결측치 처리방식',
                    component: 'option_select',
                    options: ['None', "'ignore'"],
                    options_label: ['선택 안함', '결측치 무시'],
                    default: 'None'
                }
            ]
        },
        'pd086': {
            id: 'apply',
            name: 'Apply',
            library: 'pandas',
            description: '임의 함수를 이용해 데이터 변형',
            code: '${o0} = ${i0}.apply(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy', 'Rolling']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'func',
                    type: 'var',
                    label: '적용할 함수',
                    component: 'var_select',
                    var_type: ['function'],
                    required: true
                },
                {
                    index: 1,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    default: 0
                },
                {
                    index: 2,
                    name: 'raw',
                    type: 'bool',
                    label: '함수에 전달될 객체유형',
                    default: false,
                    component: 'option_select',
                    options_label: ['Series 객체', 'ndarray 객체']
                }
            ]
        },
        'pd087': {
            id: 'applymap',
            name: 'ApplyMap',
            library: 'pandas',
            description: '임의 함수를 이용해 데이터 변형',
            code: '${o0} = ${i0}.applymap(${i1})',
            guide: [
                'df = pd.DataFrame([[1, 2.12], [3.356, 4.567]])',
                'df.applymap(lambda x: len(str(x)))',
                'df.applymap(lambda x: x**2)'
            ],
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                },
                {
                    index: 1,
                    name: 'i1',
                    type: 'var',
                    label: '대상 함수',
                    var_type: ['function']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: []
        },
        'pd088': {
            id: 'cut',
            name: 'Cut',
            library: 'pandas',
            description: '동일 길이로 나눠 범주 구성',
            code: '${o0} = pd.cut(${i0}, ${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:['var', 'list'],
                    label: '1차원 배열'
                },
                {
                    index: 1,
                    name: 'i1',
                    type:['int', 'var'],
                    label: '나눌 기준'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'right',
                    type: 'bool',
                    label: '오른쪽 기준 포함여부(이하/미만)',
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 1,
                    name: 'labels',
                    type: ['list', 'bool'],
                    label: '구간별 라벨'
                },
                {
                    index: 2,
                    name: 'precision',
                    type: 'int',
                    label: '소수점 이하 자릿수',
                    default: 3
                }
            ]
        },
        'pd089': {
            id: 'qcut',
            name: 'Qcut',
            library: 'pandas',
            description: '동일 개수로 나눠 범주 구성',
            code: '${o0} = pd.qcut(${i0}, ${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:['var', 'list'],
                    label: '1차원 배열/Series',
                    var_type: ['list', 'Series']
                },
                {
                    index: 1,
                    name: 'i1',
                    type:['int', 'var'],
                    label: '나눌 기준'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'labels',
                    type: ['list', 'bool'],
                    label: '구간별 라벨'
                },
                {
                    index: 1,
                    name: 'precision',
                    type: 'int',
                    label: '소수점 이하 자릿수',
                    default: 3
                }
            ]
        },
        'pd090': {
            id: 'sample',
            name: 'Sample',
            library: 'pandas',
            description: '',
            code: '${o0} = ${i0}.sample(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                // n과 frac은 동시에 쓸 수 없음
                {
                    index: 0,
                    name: 'n',
                    type: 'int',
                    label: '추출할 샘플 수'
                },
                {
                    index: 1,
                    name: 'frac',
                    type: 'float',
                    label: '추출할 비율'
                },
                {
                    index: 2,
                    name: 'replace',
                    type: 'bool',
                    label: '중복 추출여부',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 3,
                    name: 'weights',
                    type: ['text', 'list', 'list2d'],
                    label: '샘플마다 뽑힐 확률'
                },
                {
                    index: 4,
                    name: 'random_state',
                    type: ['var', 'int'],
                    label: '랜덤 추출 시드',
                    var_type: ['RandomState']
                },
                {
                    index: 5,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    default: 0
                }
            ]
        },
        'pd091': {
            id: 'get_dummies',
            name: 'Get Dummies',
            library: 'pandas',
            description: 'One-Hot Encoding',
            code: '${o0} = pd.get_dummies(${i0}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'prefix',
                    type: ['text', 'list', 'dict'],
                    label: '컬럼명 머릿말'
                },
                {
                    index: 1,
                    name: 'prefix_sep',
                    type: ['text'],
                    label: 'header seperator',
                    default: '_'
                },
                {
                    index: 2,
                    name: 'dummy_na',
                    type: 'bool',
                    label: '결측치 포함여부',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 3,
                    name: 'columns',
                    type: 'list',
                    label: '인코딩할 특정 컬럼'
                },
                {
                    index: 4,
                    name: 'drop_first',
                    type: 'bool',
                    label: '첫 컬럼 제외 여부',
                    default: false,
                    component: 'bool_checkbox'
                }
            ]
        },
        'pd092': {
            id: '.str',
            name: '.Str',
            library: 'pandas',
            description: '문자열의 벡터화 (문자배열에만 사용 가능)',
            code: '${o0} = ${i0}.str',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series', 'Index']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: []
        },
        'pd093': {
            id: 'var',
            name: 'Var',
            library: 'pandas',
            description: '분산 조회',
            code: '${o0} = ${i0}.var(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy', 'EWM', 'Rolling']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'skipna',
                    type: 'bool',
                    label: '결측치 제외여부',
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 2,
                    name: 'level',
                    type: 'int',
                    label: '계층 인덱스'
                },
                {
                    index: 3, 
                    name: 'ddof',
                    type: 'int',
                    label: '델타 자유도'
                },
                {
                    index: 4,
                    name: 'numeric_only',
                    type: 'var',
                    label: 'float/int/bool 컬럼만 포함',
                    component: 'option_select',
                    options: ['None', "'True'", "'False'"],
                    options_label: ['선택 안 함', 'O', 'X'],
                    default: 'None'
                }
            ]
        },
        'pd094': {
            id: 'prod',
            name: 'Prod',
            library: 'pandas',
            description: '결측치가 아닌 값들의 곱',
            code: '${o0} = ${i0}.prod(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 1,
                    name: 'skipna',
                    type: 'bool',
                    label: '결측치 제외여부',
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 2,
                    name: 'level',
                    type: 'int',
                    label: '계층 인덱스'
                },
                {
                    index: 3,
                    name: 'numeric_only',
                    type: 'var',
                    label: 'float/int/bool 컬럼만 포함',
                    component: 'option_select',
                    options: ['None', "'True'", "'False'"],
                    options_label: ['선택 안 함', 'O', 'X'],
                    default: 'None'
                },
                {
                    index: 4,
                    name: 'min_count',
                    type: 'int',
                    label: '연산을 위한 유효값의 최소 개수',
                    default: 0
                }
            ]
        },
        'pd095': {
            id: 'first',
            name: 'First',
            library: 'pandas',
            description: '결측치가 아닌 값들 중 첫 번째 값',
            code: '${o0} = ${i0}.first(${i1})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                },
                {
                    index: 1,
                    name: 'i1', // offset
                    type: ['text','var'],
                    label: '날짜 오프셋',
                    help: '1M은 1달'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [

            ]
        },
        'pd096': {
            id: 'last',
            name: 'Last',
            library: 'pandas',
            description: '결측치가 아닌 값들 중 마지막 값',
            code: '${o0} = ${i0}.last(${i1})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                },
                {
                    index: 1,
                    name: 'i1', // offset
                    type: ['text','var'],
                    label: '날짜 오프셋',
                    help: '1M은 1달'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
            ]
        },
        'pd097': {
            id: 'agg',
            name: 'Aggregation',
            library: 'pandas',
            description: '결측치가 아닌 값들 중 마지막 값',
            code: '${o0} = ${i0}.agg(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                },
                {
                    index: 1,
                    name: 'i1',
                    type: ['var', 'list', 'dict'],
                    label: '데이터 집계할 함수명',
                    options: ['sum', 'mean', 'min', 'max', 'count', 'std', 'quantile']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    default: 0
                }
            ]
        },
        'pd098': {
            id: 'transform',
            name: 'Transform',
            library: 'pandas',
            description: '',
            code: '${o0} = ${i0}.transform(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                },
                {
                    index: 1,
                    name: 'i1',
                    type: ['var', 'list', 'dict'],
                    label: '데이터 집계할 함수명',
                    options: ['sum', 'mean', 'min', 'max', 'count']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    default: 0
                }
            ]
        },
        'pd099': {
            id: 'pivot_table',
            name: 'Pivot Table',
            library: 'pandas',
            description: '집계연산한 결과물로 2차원 피봇테이블 구성',
            code: '${o0} = ${i0}.pivot_table(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'values',
                    type: 'var',
                    label: '집계할 컬럼'
                },
                {
                    index: 1,
                    name: 'index',
                    type: ['var', 'list'],
                    label: '행 인덱스로 쓸 컬럼'
                },
                {
                    index: 2,
                    name: 'columns',
                    type: ['var', 'list'],
                    label: '열 인덱스로 쓸 컬럼'
                },
                {
                    index: 3,
                    name: 'aggfunc',
                    type: ['var', 'list'],
                    label: '집계함수 목록'
                },
                {
                    index: 4,
                    name: 'fill_value',
                    type: ['var', 'int', 'float', 'bool'],
                    label: '결측치 대체값'
                },
                {
                    index: 5,
                    name: 'margins',
                    type: 'bool',
                    label: '집계 행/열 추가 여부',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 6,
                    name: 'dropna',
                    type: 'bool',
                    label: '컬럼 값이 모두 결측치일 경우 제외',
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 7,
                    name: 'margins_name',
                    type: 'text',
                    label: '합계 행/열 이름',
                    default: 'All'
                }
            ]
        },
        'pd100': {
            id: 'crosstab',
            name: 'CrossTable',
            library: 'pandas',
            description: '교차테이블 구성',
            code: '${o0} = pd.crosstab(${i0}, ${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: '행 Series/list',
                    component: 'var_select',
                    var_type: ['Series', 'list']
                },
                {
                    index: 1,
                    name: 'i1',
                    type:'var',
                    label: '열 Series/list',
                    component: 'var_select',
                    var_type: ['Series', 'list']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'values',
                    type: 'list',
                    label: '집계할 값 배열'
                },
                {
                    index: 1,
                    name: 'rownames',
                    type: 'list',
                    label: '행 이름 목록'
                },
                {
                    index: 2,
                    name: 'colnames',
                    type: 'list',
                    label: '열 이름 목록'
                },
                {
                    index: 3,
                    name: 'aggfunc',
                    type: 'var',
                    label: '집계함수',
                    options: ['sum', 'mean', 'min', 'max', 'count']
                },
                {
                    index: 4,
                    name: 'margins',
                    type: 'bool',
                    label: '집계 행/열 추가 여부',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 5,
                    name: 'margins_name',
                    type: 'text',
                    label: '합계 행/열 이름',
                    default: 'All'
                },
                {
                    index: 6,
                    name: 'dropna',
                    type: 'bool',
                    label: '컬럼 값이 모두 결측치일 경우 제외',
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 7,
                    name: 'normalize',
                    type: 'bool',
                    label: '구성비율',
                    default: true,
                    component: 'bool_checkbox'
                }
            ]
        },
        'pd101': {
            id: 'to_datetime',
            name: 'To Datetime',
            library: 'pandas',
            description: '문자열/배열을 datetime 객체로 변환',
            code: '${o0} = pd.to_datetime(${i0}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: '날짜 목록',
                    component: 'var_select',
                    var_type: ['list', 'DataFrame', 'Series', 'int', 'float', 'text', 'datetime']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'

                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'errors',
                    type: 'text',
                    label: '오류 처리방안',
                    component: 'option_select',
                    default: 'raise',
                    options: ['raise', 'ignore', 'coerce'],
                    options_label: ['오류 발생', 'NaT 값으로 설정', '입력값 그대로']
                },
                {
                    index: 1,
                    name: 'dayfirst',
                    type: 'bool',
                    label: '일자 먼저 입력',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 2,
                    name: 'yearfirst',
                    type: 'bool',
                    label: '연도 먼저 입력',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 3,
                    name: 'format',
                    type: 'text',
                    label: '날짜 형식',
                    help: '%d/%m/%Y'
                }
            ]
        },
        'pd102': {
            id: '.is_unique',
            name: 'Is Unique',
            library: 'pandas',
            description: '', // TODO:
            code: '${o0} = ${i0}.is_unique',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['Series', 'Index']
                },
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'

                }
            ],
            variable: []
        },
        'pd103': {
            id: 'resample',
            name: 'Resample',
            library: 'pandas',
            description: '', // TODO:
            code: '${o0} = ${i0}.resample(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name: 'i1',
                    type: 'var',
                    label: 'offset 문자/객체',
                    options: ['5T', '10T', '20T', '1H', '1D', '1W', '1M', 'Q', '1Y'],
                    options_label: [
                        '5분 단위', '10분 단위', '20분 단위', '1시간 단위',
                        '1일 단위', '1주일 단위', '1달 단위', '분기별', '1년 단위'
                    ]
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'

                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                }
            ]
        },
        'pd104': {
            id: 'shift',
            name: 'Shift',
            library: 'pandas',
            description: '', // TODO:
            code: '${o0} = ${i0}.shift(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Index']
                },
                {
                    index: 1,
                    name: 'i1', // periods
                    type: 'int',
                    label: '데이터 쉬프트시킬 기간'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable',
                    var_type: ['Series']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'freq',
                    type: 'var',
                    label: '오프셋',
                    options: ['M', 'D', '90T'],
                    options_label: ['월', '일', '90시간']
                },
                {
                    index: 1,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                },
                {
                    index: 2,
                    name: 'fill_value',
                    type: 'var',
                    label: '결측치 대체값'
                }
            ]
        },
        'pd105': {
            id: 'tshift',
            name: 'TShift',
            library: 'pandas',
            description: '', // TODO:
            code: '${o0} = ${i0}.tshift(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Index', 'GroupBy']
                },
                {
                    index: 1,
                    name: 'i1', // periods
                    type: 'int',
                    label: '인덱스 쉬프트시킬 기간'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable',
                    var_type: ['Series', 'DataFrame']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'freq',
                    type: 'var',
                    label: '오프셋',
                    options: ['M', 'D', '90T'],
                    options_label: ['월', '일', '90시간']
                },
                {
                    index: 1,
                    name: 'axis',
                    type: 'int',
                    label: 'axis',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                }
            ]
        },
        'pd106': {
            id: 'date_shift',
            name: 'Date Shift Operation',
            library: 'pandas',
            description: '', // TODO:
            code: '${o0} = ${i0} ${i1} ${i2}',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: '첫 번째 값(날짜/숫자)',
                    options: ['datetime', 'Day()', 'MonthEnd()']
                },
                {
                    index: 1,
                    name: 'i1', // periods
                    type: 'int',
                    label: '날짜 쉬프트 연산 유형',
                    component: 'option_select',
                    options: ['+', '-', '*', '/']

                },
                {
                    index: 2,
                    name: 'i2',
                    type:'var',
                    label: '두 번째 값(날짜/숫자)',
                    options: ['datetime', 'Day()', 'MonthEnd()']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: []
        },
        'pd107': {
            id: 'tz_localize',
            name: 'Timezone Localize',
            library: 'pandas',
            description: '지역 시간대 설정',
            code: '${o0} = ${i0}.tz_localize(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Timestamp', 'DatetimeIndex']
                },
                {
                    index: 1,
                    name: 'i1', // tz
                    type: ['text', 'var'],
                    label: '타임존',
                    options: [
                        'UTC'
                    ]
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable',
                    var_type: ['Series', 'DataFrame']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: '시간대 설정할 행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    default: 0
                },
                {
                    index: 1,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '시간대 설정할 계층'
                },
                {
                    index: 2,
                    name: 'copy',
                    type: 'bool',
                    label: '깊은 복사 여부',
                    component: 'bool_checkbox',
                    default: true
                }
            ]
        },
        'pd108': {
            id: 'tz_convert',
            name: 'Timezone Convert',
            library: 'pandas',
            description: '지역 시간대 변경',
            code: '${o0} = ${i0}.tz_convert(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Timestamp', 'DatetimeIndex']
                },
                {
                    index: 1,
                    name: 'i1', // tz
                    type: ['text', 'var'],
                    label: '타임존',
                    options: [
                        'UTC',
                        'Asia/Seoul',
                        'America/New_York',
                        'Europe/Berlin'
                    ]
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable',
                    var_type: ['Series', 'DataFrame']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: '시간대 설정할 행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    default: 0
                },
                {
                    index: 1,
                    name: 'level',
                    type: ['int', 'text'],
                    label: '시간대 설정할 계층'
                },
                {
                    index: 2,
                    name: 'copy',
                    type: 'bool',
                    label: '깊은 복사 여부',
                    component: 'bool_checkbox',
                    default: true
                }
            ]
        },
        'pd109': {
            id: 'Timestamp',
            name: 'Timestamp',
            library: 'pandas',
            description: 'Timestamp 객체 생성',
            code: '${o0} = pd.Timestamp(${v})',
            input: [
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'ts_input',
                    type: ['var', 'text', 'int', 'float'],
                    label: 'Timestamp로 변환할 값'
                },
                {
                    index: 1,
                    name: 'freq',
                    type: ['text', 'var'],
                    label: 'Timestamp 오프셋'
                },
                {
                    index: 2,
                    name: 'year',
                    type: 'int',
                    label: '연도'
                },
                {
                    index: 3,
                    name: 'month',
                    type: 'int',
                    label: '월'
                },
                {
                    index: 4,
                    name: 'day',
                    type: 'int',
                    label: '일'
                },
                {
                    index: 5,
                    name: 'hour',
                    type: 'int',
                    label: '시',
                    default: 0
                },
                {
                    index: 6,
                    name: 'minute',
                    type: 'int',
                    label: '분',
                    default: 0
                },
                {
                    index: 7,
                    name: 'second',
                    type: 'int',
                    label: '초',
                    default: 0
                },
                {
                    index: 8,
                    name: 'tz',
                    type: ['text', 'var'],
                    label: '시간대'
                }
            ]
        },
        'pd110': {
            id: 'period_range',
            name: 'Period Range',
            library: 'pandas',
            description: '',
            code: '${o0} = pd.period_range(${v})',
            input: [
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: 
            [
                {
                    index: 0,
                    name: 'start',
                    type: 'text',
                    label: '범위 시작점'
                },
                {
                    index: 1,
                    name: 'end',
                    type: 'text',
                    label: '범위 종료점'
                },
                {
                    index: 2,
                    name: 'periods',
                    type: 'int',
                    label: '생성할 범위 수'
                },
                {
                    index: 3,
                    name: 'freq',
                    type: ['text', 'var'],
                    label: '빈도수'
                },
                {
                    index: 4,
                    name: 'name',
                    type: 'text',
                    label: 'PeriodIndex 이름'
                }
            ]
        },
        'pd111': {
            id: 'asfreq',
            name: 'as Frequency',
            library: 'pandas',
            description: '', // TODO:
            code: '${o0} = ${i0}.asfreq(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Period', 'PeriodIndex', 'Resampler']
                },
                {
                    index: 1,
                    name: 'i1', // freq
                    type: ['text', 'var'],
                    label: '빈도 오프셋',
                    options: [
                        'UTC',
                        'Asia/Seoul',
                        'America/New_York',
                        'Europe/Berlin'
                    ]
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable',
                    var_type: ['Series', 'DataFrame']
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'method',
                    type: 'var',
                    label: '빈 구간 채우는 방식',
                    help: 'ffill:이전 값으로 채우기\nbfill:뒤에 있는 값으로 채우기',
                    component: 'option_select',
                    default: 'None',
                    options: ['None', "'ffill'", "'bfill'"],
                    options_label: ['선택 안 함', '이전 값으로 채우기', '이후 값으로 채우기']
                },
                {
                    index: 1,
                    name: 'normalize',
                    type: 'bool',
                    label: '결과 인덱스 초기화 여부',
                    component: 'bool_checkbox',
                    default: false
                },
                {
                    index: 2,
                    name: 'fill_value',
                    type: 'var',
                    label: '결측치 대체값'
                }
            ]
        },
        'pd112': {
            id: 'to_period',
            name: 'To Period',
            library: 'pandas',
            description: 'Timestamp에서 Period로 변환',
            code: '${o0} = ${i0}.to_period(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Timestamp', 'DatetimeIndex']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'freq',
                    label: '주기',
                    type: 'text',
                    options: ['s', 'T', 'H', 'D', 'B', 'W', 'W-MON', 'MS', 'M', 'BMS', 'BM'],
                    options_label: ['초', '분', '시간', '일', '주말이 아닌 평일', '주(일요일)', '주(월요일)', '각 달의 첫날', '각 달의 마지막 날', '평일 중 각 달의 첫날', '평일 중 각 달의 마지막 날']
                },
                {
                    index: 1,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    default: 0
                },
                {
                    index: 2,
                    name: 'copy',
                    type: 'bool',
                    label: '깊은 복사 여부',
                    component: 'bool_checkbox',
                    default: true
                }
            ]
        },
        'pd113': {
            id: 'to_timestamp',
            name: 'To Timestamp',
            library: 'pandas',
            description: 'PeriodIndex를 DatetimeIndex로 변환',
            code: '${o0} = ${i0}.to_timestamp(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'Timestamp', 'DatetimeIndex']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'freq',
                    label: '빈도 오프셋',
                    type: 'text',
                    options: ['s', 'T', 'H', 'D', 'B', 'W', 'W-MON', 'MS', 'M', 'BMS', 'BM'],
                    options_label: ['초', '분', '시간', '일', '주말이 아닌 평일', '주(일요일)', '주(월요일)', '각 달의 첫날', '각 달의 마지막 날', '평일 중 각 달의 첫날', '평일 중 각 달의 마지막 날']
                },
                {
                    index: 1,
                    name: 'how',
                    label: '', // TODO:
                    type: 'text',
                    component: 'option_select',
                    options : ['start', 'end'],
                    options_label: ['시작점', '종료점']
                },
                            {
                    index: 2,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    default: 0
                },
                {
                    index: 3,
                    name: 'copy',
                    type: 'bool',
                    label: '깊은 복사 여부',
                    component: 'bool_checkbox',
                    default: true
                }
            ]
        },
        'pd114': {
            id: 'PeriodIndex',
            name: 'PeriodIndex',
            library: 'pandas',
            description: 'PeriodIndex 생성',
            code: '${o0} = pd.PeriodIndex(${v})',
            input: [
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'data',
                    type: 'list',
                    label: 'PeriodIndex 데이터'
                },
                {
                    index: 1, 
                    name: 'copy',
                    type: 'bool',
                    label: '깊은 복사 여부',
                    component: 'bool_checkbox',
                    default: false
                },
                {
                    index: 2,
                    name: 'freq',
                    type: 'text',
                    label: '빈도수 오프셋',
                    component: 'option_select',
                    options: ['s', 'T', 'H', 'D', 'B', 'W', 'W-MON', 'MS', 'M', 'BMS', 'BM'],
                    options_label: ['초', '분', '시간', '일', '주말이 아닌 평일', '주(일요일)', '주(월요일)', '각 달의 첫날', '각 달의 마지막 날', '평일 중 각 달의 첫날', '평일 중 각 달의 마지막 날']
                },
                {
                    index: 3,
                    name: 'year',
                    type: ['int', 'list', 'Series'],
                    label: '연도'
                },
                {
                    index: 4,
                    name: 'month',
                    type: ['int', 'list', 'Series'],
                    label: '월'
                },
                {
                    index: 5,
                    name: 'quarter',
                    type: ['int', 'list', 'Series'],
                    label: '분기'
                },
                {
                    index: 6,
                    name: 'day',
                    type: ['int', 'list', 'Series'],
                    label: '일'
                },
                {
                    index: 7,
                    name: 'hour',
                    type: ['int', 'list', 'Series'],
                    label: '시',
                    default: 0
                },
                {
                    index: 8,
                    name: 'minute',
                    type: ['int', 'list', 'Series'],
                    label: '분',
                    default: 0
                },
                {
                    index: 9,
                    name: 'second',
                    type: ['int', 'list', 'Series'],
                    label: '초',
                    default: 0
                },
                {
                    index: 10,
                    name: 'tz',
                    type: ['text', 'var'],
                    label: '시간대'
                }
            ]
        },
        'pd115': {
            id: 'rolling',
            name: 'Rolling',
            library: 'pandas',
            description: '시계열 롤링 통계',
            code: '${o0} = ${i0}.rolling(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name: 'i1', // window
                    type: ['int', 'text'],
                    label: '통계낼 데이터 수'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'min_periods',
                    type: 'int',
                    label: '유효값 최소 개수',
                    help: '범위 내 데이터가 최소 개수보다 많으면 연산에 포함한다'
                },
                {
                    index: 1,
                    name: 'center',
                    type: 'bool',
                    label: '중간을 기준으로 이동',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 2,
                    name: 'win_type',
                    type: 'text',
                    label: '롤링뷰 유형',
                    component: 'option_select',
                    options: ['boxcar', 'triang', 'blackman', 'hamming', 'bartlett', 'parzen', 'bohman', 'blackmanharris', 'nuttall', 'barthann']

                },
                {
                    index: 3,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    default: 0
                }
            ]
        },
        'pd116': {
            id: 'ewm',
            name: 'EWM',
            library: 'pandas',
            description: '지수 이동평균 계산',
            code: '${o0} = ${i0}.ewm(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'com',
                    type: 'float',
                    label: '', // TODO:
                    help: 'com≥0 일 때, α=1/(1+com)'
                },
                {
                    index: 1,
                    name: 'span',
                    type: 'float',
                    label: '기간', // TODO:
                    help: 'span≥1 일 때, α=2/(span+1)'
                },
                {
                    index: 2,
                    name: 'halflife',
                    type: 'float',
                    label: '', // TODO:
                    help: 'halflife>0 일 때, α=1−exp(log(0.5)/halflife)'
                },
                {
                    index: 3,
                    name: 'alpha',
                    type: 'float',
                    label: '', // TODO:
                    help: '0<α≤1'
                },
                {
                    index: 4,
                    name: 'min_periods',
                    type: 'int',
                    label: '', // TODO:
                    help: '',
                    default: 0
                },
                {
                    index: 5,
                    name: 'adjust',
                    type: 'bool',
                    label: '', // TODO:
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 6,
                    name: 'ignore_na',
                    type: 'bool',
                    label: '결측치 무시',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 7,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    default: 0,
                    component: 'option_select',
                    options: [0, 1],
                    options_label: ['row', 'column']
                }
            ]
        },
        'pd117': {
            id: 'pct_change',
            name: 'PCT Change',
            library: 'pandas',
            description: '전일/또는 어떤 기간에서의 변화율 계산',
            code: '${o0} = ${i0}.pct_change(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'periods',
                    type: 'int',
                    label: '', // TODO:
                    default: 1
                },
                {
                    index: 1,
                    name: 'fill_method',
                    type: 'text',
                    label: '결측치 대체방식', // TODO:
                    default: 'ffill',
                    options: ["'ffill'", "'bfill'"],
                    options_label: ['이전 값으로 채우기', '이후 값으로 채우기']
                },
                {
                    index: 2,
                    name: 'limit',
                    type: 'int',
                    label: '' // TODO:
                },
                {
                    index: 3,
                    name: 'freq',
                    type: ['text','var'],
                    label: '빈도 오프셋',
                    options: ['s', 'T', 'H', 'D', 'B', 'W', 'W-MON', 'MS', 'M', 'BMS', 'BM'],
                    options_label: ['초', '분', '시간', '일', '주말이 아닌 평일', '주(일요일)', '주(월요일)', '각 달의 첫날', '각 달의 마지막 날', '평일 중 각 달의 첫날', '평일 중 각 달의 마지막 날']
                },
            ]
        },
        'pd118': {
            id: 'corr',
            name: 'Correlation',
            library: 'pandas',
            description: '컬럼 간 상관관계 연산',
            code: '${o0} = ${i0}.corr(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'GroupBy', 'EWM']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'method',
                    type: ['text', 'var'],  // 옵션 또는 callable(arr, arr)
                    label: '상관관계 방식',
                    default: 'pearson',
                    component: 'option_select',
                    options: ['pearson', 'kendall', 'spearman'],
                },
                {
                    index: 1,
                    name: 'min_periods',
                    type: 'int',
                    label: '유효한 컬럼쌍 최소 개수' // FIXME:
                }
            ]
        },
        'pd119': {
            id: 'corrwith',
            name: 'Correlation With',
            library: 'pandas',
            description: '상관관계 연산',
            code: '${o0} = ${i0}.corrwith(${i1}${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'DataFrameGroupBy']
                },
                {
                    index: 1,
                    name: 'i1',
                    type:'var',
                    label: '비교할 DataFrame/DataFrameGroupBy',
                    component: 'var_select',
                    var_type: ['DataFrame', 'DataFrameGroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'axis',
                    type: 'int',
                    label: '행/열',
                    default: 0,
                    options: [0, 1],
                    options_label: ['row', 'column'],
                    component: 'option_select'
                },
                {
                    index: 1,
                    name: 'drop',
                    type: 'bool',
                    label: '빈 인덱스 제외',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 2,
                    name: 'method',
                    type: ['text', 'var'],  // 옵션 또는 callable(arr, arr)
                    label: '상관관계 방식',
                    default: 'pearson',
                    component: 'option_select',
                    options: ['pearson', 'kendall', 'spearman'],
                }
            ]
        },
        'pd120': {
            id: 'cov',
            name: 'Covariance',
            library: 'pandas',
            description: '모든 변수 간 공분산 계산',
            code: '${o0} = ${i0}.cov(${v})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'target variable',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series', 'DataFrameGroupBy']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'min_periods',
                    type: 'int',
                    label: '유효한 컬럼쌍 최소 개수' // FIXME:
                }
            ]
        },
        'pd121': {
            id: 'plot',
            name: 'Plot',
            library: 'pandas',
            description: '차트 생성',
            code: '${o0} = ${i0}.plot(${v}${etc})',
            input: [
                {
                    index: 0,
                    name: 'i0',
                    type:'var',
                    label: 'Pandas Object',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'kind',
                    type: 'text',
                    label: 'chart type',
                    default: 'line',
                    component: 'option_select',
                    options: ['line', 'bar', 'barh', 'hist', 'box', 'kde', 'area', 'pie', 'scatter', 'hexbin'],
                    options_label: ['선', '막대', '가로 막대', '히스토그램', '박스플롯', 'Kernel Density Estimation', 'Area', '파이', 'Scatter', 'Hexbin']
                },
                {
                    index: 1,
                    name: 'title',
                    type: ['text', 'list'],
                    label: 'chart title'
                },
                {
                    index: 2,
                    name: 'figsize',
                    type: 'tuple',
                    label: 'figure size',
                    placeholder: '(너비, 높이)'
                },
                {
                    index: 3,
                    name: 'fontsize',
                    type: 'int',
                    label: 'font size'
                },
                {
                    index: 4,
                    name: 'colormap',
                    type: 'text',
                    label: 'color map',
                    component: 'option_select',
                    options: [
                        'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'
                    ],
                    options_label: [
                        'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'
                    ]
                },
                {
                    index: 5,
                    name: 'grid',
                    type: 'bool',
                    label: 'show grid',
                    component: 'bool_checkbox',
                    default: false
                },
                {
                    index: 6,
                    name: 'legend',
                    type: 'bool',
                    label: 'show legend',
                    component: 'bool_checkbox',
                    default: false
                },
                {
                    index: 7,
                    name: 'rot',
                    type: 'int',
                    label: 'x label rotation'
                },
                {
                    index: 8,
                    name: 'xlabel',
                    type: 'list',
                    label: 'x label'
                },
                {
                    index: 9,
                    name: 'ylabel',
                    type: 'list',
                    label: 'y label'
                },
                {
                    index: 10,
                    name: 'xlim',
                    type: ['var', 'list'], //tuple
                    label: 'x limit',
                    placeholder: '(x축 시작점, x축 종료점)'
                },
                {
                    index: 11,
                    name: 'ylim',
                    type: ['var', 'list'], //tuple
                    label: 'y limit',
                    placeholder: '(y축 시작점, y축 종료점)'
                },
                {
                    index: 12,
                    name: 'xticks',
                    type: 'list',
                    label: 'x ticks',
                    placeholder: '["틱1", "틱2"]',
                    description: 'x축에 표시되는 지점 별 라벨 목록'
                },
                {
                    index: 13,
                    name: 'yticks',
                    type: 'list',
                    label: 'y ticks',
                    placeholder: '["틱1", "틱2"]',
                    description: 'y축에 표시되는 지점 별 라벨 목록'
                },
                {
                    index: 14,
                    name: 'style',
                    type: ['list', 'dict'],
                    label: 'style',
                    placeholder: '["-", "--", "-.", ":"]',
                    help: '컬럼 수와 목록 개수가 맞아야 합니다'
                },
                {
                    index: 15,
                    name: 'x',
                    type: ['text', 'int'],
                    label: 'x column'
                },
                {
                    index: 16,
                    name: 'y',
                    type: ['text', 'int'],
                    label: 'y column'
                },
                {
                    index: 17,
                    name: 'subplots',
                    type: 'bool',
                    label: 'subplots per column',
                    default: false,
                    component: 'bool_checkbox'
                },
                {
                    index: 18, 
                    name: 'layout',
                    type: 'tuple',
                    label: 'subplot layout',
                    placeholder: '(row, column)'
                },
                {
                    index: 19,
                    name: 'use_index',
                    type: 'bool',
                    label: 'use index on x ticks',
                    default: true,
                    component: 'bool_checkbox'
                },
                {
                    index: 20,
                    name: 'stacked',
                    type: 'bool',
                    label: 'show stacked',
                    default: false,//true in area
                    component: 'bool_checkbox'
                }
            ],
        },
        'pd122': {
            id: 'sampleCsv',
            name: 'Sample Csv',
            library: 'pandas',
            description: '샘플 데이터 불러오기',
            code: '${o0} = pd.read_csv(${i0}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'text',
                    label: 'sample file',
                    component: 'option_select',
                    options: [
                        'iris.csv', 'Titanic_train.csv', 'Titanic_test.csv', 'cancer.csv',
                        'fish.csv', 'accidentData.csv', 'campusRecruitment.csv', 'houseData_500.csv',
                        'lolRankedData_500.csv', 'weatherData_500.csv', 'welfareCenter.csv',
                        'mnist_train_1000.csv'
                    ],
                    options_label: [
                        'iris', 'Titanic_train', 'Titanic_test', 'cancer',
                        'fish', 'accidentData', 'campusRecruitment', 'houseData_500',
                        'lolRankedData_500', 'weatherData_500', 'welfareCenter',
                        'mnist_train_1000'
                    ]
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable',
                    required: true
                }
            ]
        },
        'pd123': {
            id: 'readExcel',
            name: 'Read Excel',
            library: 'pandas',
            description: '엑셀 파일을 불러와 DataFrame 생성',
            code: '${o0} = pd.read_excel(${i0}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'text',
                    label: 'file path',
                    component: 'file'
                }
            ],
            output: [
                {
                    index: 0,
                    name:'o0',
                    type:'var',
                    label:'return variable'
                }
            ],
            variable: [
                {
                    index: 0,
                    name: 'sheet_name',
                    type: 'text',
                    label: '시트명'
                }
            ]
        },
        'pd124': {
            id: 'to_excel',
            name: 'To Excel',
            library: ['pandas', 'xlwt', 'openpyxl'], // TODO: required packages
            description: 'DataFrame을 excel 파일로 작성',
            code: '${i0}.to_excel(${i1}${v})',
            input: [
                {
                    index: 0,
                    name:'i0',
                    type:'var',
                    label: 'Pandas Object',
                    component: 'var_select',
                    var_type: ['DataFrame', 'Series']
                },
                {
                    index: 1,
                    name:'i1',
                    type:'text',
                    label: 'file path',
                    component: 'file'
                }
            ],
            output: [
            ],
            variable: [
                {
                    index: 0,
                    name: 'sheet_name',
                    type: 'text',
                    label: '시트명'
                }
            ]
        },
    }

    return {
        _PANDAS_FUNCTION: _PANDAS_FUNCTION
    };
});