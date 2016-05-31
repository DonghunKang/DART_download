s = """	
		// 1
		treeNode1 = new Tree.TreeNode({
			text: "정 정 신 고 (보고)",
			id: "12",
			cls: "text",
			listeners: {
				click: function() {viewDoc('20070716000189', '1679444', '12', '516', '114462', 'dart2.dtd');}
			}
		});
		cnt++;
		
		treeRoot.appendChild(treeNode1);
		
	
		// 2
		treeNode1 = new Tree.TreeNode({
			text: "사 업 설 명 서",
			id: "1112",
			cls: "text",
			listeners: {
				click: function() {viewDoc('20070716000189', '1679444', '1112', '115000', '2330', 'dart2.dtd');}
			}
		});
		cnt++;
		
		treeRoot.appendChild(treeNode1);
		
			
			
		
	
		// 3
		treeNode1 = new Tree.TreeNode({
			text: "대표이사등의 확인ㆍ서명",
			id: "1141",
			cls: "text",
			listeners: {
				click: function() {viewDoc('20070716000189', '1679444', '1141', '117330', '26128', 'dart2.dtd');}
			}
		});
		cnt++;
		
		treeRoot.appendChild(treeNode1);
		
	
		// 4
		treeNode1 = new Tree.TreeNode({
			text: "본        문",
			id: "1361",
			cls: "text",
			listeners: {
				click: function() {viewDoc('20070716000189', '1679444', '1361', '143458', '1182087', 'dart2.dtd');}
			}
		});
		cnt++;
		
		treeRoot.appendChild(treeNode1);
		
"""

s[s.find("(")+1:s.find(")")]