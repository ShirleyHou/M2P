clc
clear

javaclasspath('javaclass');


%%%%%%%%%%%%%%%%%
% load('links_nodes.mat','links','nodes')
% load('demand_medium.mat','demand')

% % nodes_formatted=zeros(size(nodes,1),3); %initialization
% % for i=1:1:size(nodes,1)
% %     
% %     nodes_formatted(i,:)=[nodes(i,1).ID,nodes(i,1).X,nodes(i,1).Y];
% %     
% % end
% % 
% % links_formatted=[];
% % for i=1:1:size(links,1)
% %     
% %     links_formatted=[links_formatted;[i,links(i,1).INODE,links(i,1).JNODE,links(i,1).LENGTH,60,links(i,1).DATA3,links(i,1).LANES*120]]; %60 as km/h free flow speed, 120 veh/km as k_jam
% %     
% % end
% % save('links_nodes_formatted.mat','links_formatted','nodes_formatted')

% load('links_nodes_medium.mat','links_formatted','nodes_formatted')
% 
% %step 0: convert ITLS demand data to fit MSA format (ODmatrices)
% node_TZ=zeros(size(nodes,1),2);
% for i=1:1:size(nodes,1)
%     node_TZ(i,:)=[nodes(i,1).ID,nodes(i,1).TZ_CODE11];
% end
% % % 
% demand_formatted=[]; % formattign demand to add destination node
% for i=1:1:size(demand,1)
%     
%     DTZ=demand(i,4); % this is destination TZ
%     nodes_in_DTZ=node_TZ(find(node_TZ(:,2)==DTZ),1); % nodes within DTZ
%     %%%nodes_in_DTZ=nodes_in_DTZ(randperm(length(nodes_in_DTZ))); %random shuffeling
%     
%     for j=1:1:length(nodes_in_DTZ)
%         if nodes_in_DTZ(j)~=demand(i,5)
%             demand_formatted=[demand_formatted;[demand(i,5),nodes_in_DTZ(j),demand(i,6:end)]]; % adding destination node
%             break;
%         end
%     end
%     
% end
% save('demand_formatted_medium.mat','demand_formatted')
% % 
% % 
% no_nodes=size(nodes_formatted,1);
% ODmatrices=cell(1,size(demand_formatted,2)-2);
% for i=1:1:size(ODmatrices,2) % demand time slices
%     ODmatrices{1,i}=sparse(no_nodes,no_nodes);
%     
%     for j=1:1:size(demand_formatted,1)
%         O_node=find(nodes_formatted(:,1)==demand_formatted(j,1)); %index finding
%         D_node=find(nodes_formatted(:,1)==demand_formatted(j,2)); %index finding
%         ODmatrices{1,i}(O_node,D_node)=demand_formatted(j,i+2); % creating demand entries
%     end
%     
% end
% save('demand_formatted_medium.mat','demand_formatted','ODmatrices')

%load('demand_formatted.mat','demand_formatted','ODmatrices')

% id=links_formatted(:,1);
% for i=1:1:size(links_formatted,1)
%     fromNode(i,1)=find(nodes_formatted(:,1)==links_formatted(i,2)); %index finding
%     toNode(i,1)=find(nodes_formatted(:,1)==links_formatted(i,3)); %index finding
% end
% length=links_formatted(:,4);
% freeSpeed=links_formatted(:,5);
% capacity=links_formatted(:,6);
% kJam=links_formatted(:,7);
% links=table(id,fromNode,toNode,length,freeSpeed,capacity,kJam);
% 
% original_node_id=nodes_formatted(:,1);
% id=[1:1:size(nodes_formatted,1)]';
% xco=nodes_formatted(:,2);
% yco=nodes_formatted(:,3);
% nodes=table(id,xco,yco);
% 
% save('info_medium.mat','nodes','links','ODmatrices')
% % % 
% [nodes,links,ODmatrices]=buildDummyNodesAndLinks(nodes,links,ODmatrices); % this function creats dummy origin and destination nodes and dummy connectors
% save('info2_medium.mat','nodes','links','ODmatrices')
% 
load('info2_small.mat','nodes','links','ODmatrices')

%plotNetwork(nodes,links,true,[]);

%%% Setup the simulation
% Before the simulation can be run the time interval has to be set and the
% total number of time steps has to be defined.
%

%setup the time interval and total number of time steps
dt = 20;
totT = round(20/dt);

timeSeries=0:0.5:0.5*(size(ODmatrices,2)-1); %matrix of 1*size(ODmatrices)

% % %build the full ODmatrix
%tic
%[ODmatrix,origins,destinations] = buildODmatrix(ODmatrices,timeSeries,dt,totT);
%elapsedtime=toc
%save('info3_medium.mat','nodes','links','ODmatrix','origins','destinations')
load('info3_small.mat','nodes','links','ODmatrix','origins','destinations')
%load('info3.mat','nodes','links','ODmatrix','origins','destinations')
%%save('/home/mram8091/mram8091/R2017a/info333.mat','nodes','links','elapsedtime','ODmatrix','origins','destinations')
%% Setup the dynamic equilibrium simulation
% The routing behavior in the dynamic user equilibrium is aggregated over
% larger time intervals to speed up computation. It is believed that the
% route choice time intervals varies with a much lower frequency in reality
% than the typical interval of a simulation. As travel time varies
% continuously over the route choice interval, not all vehicles within the
% same route choice interval experience the same travel time. Hence, the
% modeler should select a travel time that is representative for the entire
% route choice interval, e.g. that of the first/middle/last vehicle to
% depart within that interva.
%

%time interval for the route choice
rc_dt = 10*dt;
max_it = 1;

%Initialize the travel time aggragation for route choice behaviour
rc_agg = 'last'
%last: last vehicle of the route choice interval (standard)
%middle: middle vehicle of the route choice interval
%first: first vehicle of the route choice interval

%run DTA with deterministic route choice and MSA averaging
tic
[cvn_up,cvn_down,TF] = DTA_MSA(nodes,links,origins,destinations,ODmatrix,dt,totT,rc_dt,max_it,rc_agg);
aaa=toc
save('info4_medium.mat','cvn_up','cvn_down','TF','aaa')

%% Transform CVN values to travel times
% The upstream and dowsntream CVN functions of the link transmission model
% are transformed into travel times for every link in the network. The
% travel times are compared for the main route (from split to merge) and
% the alternative route.
%calculate the simulated travel times
% tic
[simTT] = cvn2tt(sum(cvn_up,3),sum(cvn_down,3),dt,totT,links);
% aaaa=toc
% save('/home/mram8091/mram8091/R2017a/all2.mat')
% figure
% plot(dt*(0:1:totT),simTT')
% xlim([0,dt*totT])
% xlabel('Time [h]')
% ylabel('Travel time [h]')
