<p class="has-line-data" data-line-start="1" data-line-end="2">(PROBLEM STATEMENT)</p>
<p class="has-line-data" data-line-start="3" data-line-end="4">Q. Create an api using django-rest framework that will connect to the given database and query the given table.</p>
<p class="has-line-data" data-line-start="5" data-line-end="6">Tables described here are for example it should work for any existing table or database inside the database server. It should connect to the given database and access the given table, assume that there can be multiple  databases in the same database server and inside all these databases there are multiple tables.Create post requests with the payloads given below :</p>
<p class="has-line-data" data-line-start="7" data-line-end="8">Payload Example:</p>
<pre><code>{
   &quot;database_name&quot;: &quot;database1&quot;,
   &quot;data&quot;: {
       &quot;table_name&quot;: &quot;table1&quot;,
   }
}
</code></pre>
<ol>
<li class="has-line-data" data-line-start="16" data-line-end="18">The above query should  connect to database <code>database1</code> and create an equivalent sql as SELECT * FROM <code>table1</code> and return the result like given below :</li>
</ol>
<p class="has-line-data" data-line-start="18" data-line-end="19">Payload Example:</p>
<pre><code>{
   &quot;column&quot;: [
       &quot;userid&quot;,
       &quot;uploaded_time&quot;,
       &quot;city&quot;,
       &quot;price&quot;,
       &quot;year&quot;,
       &quot;county_name&quot;,
       &quot;state_code&quot;,
       &quot;state_name&quot;
   ],
   &quot;data&quot;: [
       [
           &quot;awadhesh kumar&quot;,
           &quot;2020-03-23T12:23:47&quot;,
           &quot;marshall&quot;,
           11900,
           2010,
           &quot;Lincoln&quot;,
           &quot;SD&quot;,
           &quot;South Dakota&quot;
       ], 
       [
       &quot;awadhesh kumar&quot;,
           &quot;2020-03-23T12:23:47&quot;,
           &quot;marshall&quot;,
           2800,
           2004,
           &quot;Osceola&quot;,
           &quot;IA&quot;,
           &quot;Iowa&quot;
       ]
   ],
   &quot;length&quot;: 2
}
</code></pre>
<ol start="3">
<li class="has-line-data" data-line-start="56" data-line-end="58">We should be able to select only required fields with the following request :</li>
</ol>
<p class="has-line-data" data-line-start="58" data-line-end="59">Payload Example:</p>
<pre><code>{
   &quot;database_name&quot;: &quot;database1&quot;,
   &quot;data&quot;: {
       &quot;select_list&quot;: [
           {
               &quot;column&quot;: &quot;city&quot;
           },
           {
               &quot;column&quot;: &quot;price&quot;
           }
       ],
       &quot;worksheet_id&quot;: &quot;table1&quot;
   }
}
</code></pre>
<p class="has-line-data" data-line-start="76" data-line-end="77">with equivalent SQL like SELECT <code>table1</code>.city, <code>table1</code>.price FROM `table1 and the result as :</p>
<pre><code>{
   &quot;column&quot;: [
       &quot;city&quot;,
       &quot;price&quot;
   ],
   &quot;data&quot;: [
       [
           &quot;marshall&quot;,
           11900
       ],
       [
           &quot;marshall&quot;,
           2800
       ]
   ],
   &quot;length&quot;: 2
}
</code></pre>
<ol start="3">
<li class="has-line-data" data-line-start="96" data-line-end="98">We should be able to aggregate on different fields and group by on different fields</li>
</ol>
<p class="has-line-data" data-line-start="98" data-line-end="99">Payload Example:</p>
<pre><code>{
   &quot;database_name&quot;: &quot;database1&quot;,
   &quot;data&quot;: {
       &quot;aggregate&quot;: [
           {
               &quot;column&quot;: &quot;price&quot;,
               &quot;type&quot;: &quot;sum&quot;
           }
       ],
       &quot;groupby&quot;: [
           {
               &quot;column&quot;: &quot;city&quot;
           }
       ],
       &quot;worksheet_id&quot;: &quot;table1&quot;,
   }
}
</code></pre>
<p class="has-line-data" data-line-start="120" data-line-end="121">With equivalent SQL</p>
<pre><code>SELECT `table`.city, sum(`table`.price) AS sum_of_price 
FROM `table` 
GROUP BY `table`.city 
</code></pre>
<p class="has-line-data" data-line-start="126" data-line-end="127">Where we can add or delete different columns in aggregate and group by also different aggregate functions like (sum,avg,count,min,max and distinct count ) should work.</p>
<p class="has-line-data" data-line-start="130" data-line-end="131">Result will be:</p>
<pre><code>{
   &quot;column&quot;: [
       &quot;city&quot;,
       &quot;sum_of_price&quot;
   ],
   &quot;data&quot;: [
       [
           null,
           44.0
       ],
       [
           &quot;chambersburg&quot;,
           43200.0
       ]
   ],
   &quot;length&quot;: 2
}
</code></pre>
