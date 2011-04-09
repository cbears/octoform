<DIV style='margin: 5px; background: #eeffee; border: solid 1px #baffba; padding: 7px;' 
id='${questionNumber}'>
  ${q}
  ${content}
  <a href = "#${questionNumber}" style="text-decoration:none;">&nbsp;</a>
  <BUTTON
	 tabindex="0"
	 id='mRem_id_${questionNumber}'
	 dojoType="dijit.form.Button"
	 type='submit'
	 value='${questionNumber}'
	 label='Remove Row'
	 name="miniPageDel"
	 onclick='dojo.byId("mRem_id_${questionNumber}").value="${questionNumber}"'
	 >
	 </BUTTON>
  <BUTTON
	 tabindex="0"
	 id='mAdd_id_${questionNumber}'
	 dojoType="dijit.form.Button"
	 type='submit'
	 value='${questionNumber}'
	 label='Add Row'
	 name="miniPageAdd"
	 onclick='dojo.byId("mAdd_id_${questionNumber}").value="${questionNumber}"'
	 >
	 </BUTTON>
</DIV>
