clc
clear
close all
load small_case.mat
javaclasspath('javaclass');

%%%%%%%%%%%%%%%%%

% load('links_nodes.mat','links','nodes')
% load('demand.mat','demand')

% no_nodes=size(nodes,1);
% ODmatrices=cell(1,size(demand,2)-2);
% parfor i=1:1:size(ODmatrices,2) % demand time slices
%     ODmatrices{1,i}=sparse(no_nodes,no_nodes);
%     
%     for j=1:1:size(demand,1)
%         O_node=find(table2array(nodes(:,1))==demand(j,1)); %index finding
%         D_node=find(table2array(nodes(:,1))==demand(j,2)); %index finding
%         ODmatrices{1,i}(O_node,D_node)=demand(j,i+2); % creating demand entries
%         j
%     end
%     i
% end
% save('info_amir_1.mat')
id=links(:,1);
for i=1:1:size(links,1)
    fromNode(i,1)=find(nodes(:,1)==links(i,2)); %index finding
    toNode(i,1)=find(nodes(:,1)==links(i,3)); %index finding
end
length=links(:,4);
freeSpeed=links(:,5);
capacity=links(:,6);
kJam=links(:,7);
links=table(id,fromNode,toNode,length,freeSpeed,capacity,kJam);

original_node_id=nodes(:,1);
id=[1:1:size(nodes,1)]';
xco=nodes(:,2);
yco=nodes(:,3);
nodes=table(id,xco,yco);
[nodes,links,ODmatrices]=buildDummyNodesAndLinks(nodes,links,ODmatrices); % this function creats dummy origin and destination nodes and dummy connectors

%%% Setup the simulation
% Before the simulation can be run the time interval has to be set and the
% total number of time steps has to be defined.

%setup the time interval and total number of time steps
dt = 0.5;
totT = round(20/dt);

timeSeries=0:0.5:0.5*(size(ODmatrices,2)-1); %matrix of 1*size(ODmatrices)
% % %build the full ODmatrix
[ODmatrix,origins,destinations] = buildODmatrix(ODmatrices,timeSeries,dt,totT);
save('info_amir_2.mat');
%% Setup the dynamic equilibrium simulation
% The routing behavior in the dynamic user equilibrium is aggregated over
% larger time intervals to speed up computation. It is believed that the
% route choice time intervals varies with a much lower frequency in reality
% than the typical interval of a simulation. As travel time varies
% continuously over the route choice interval, not all vehicles within the
% same route choice interval experience the same travel time. Hence, the
% modeler should select a travel time that is representative for the entire
% route choice interval, e.g. that of the first/middle/last vehicle to
% depart within that interval.
%

%time interval for the route choice
rc_dt = 10*dt;
max_it = 10;

%Initialize the travel time aggragation for route choice behaviour
rc_agg = 'last';
%last: last vehicle of the route choice interval (standard)
%middle: middle vehicle of the route choice interval
%first: first vehicle of the route choice interval

%run DTA with deterministic route choice and MSA averaging
[cvn_up,cvn_down,TF] = DTA_MSA(nodes,links,origins,destinations,ODmatrix,dt,totT,rc_dt,max_it,rc_agg);

%% Transform CVN values to travel times
% The upstream and dowsntream CVN functions of the link transmission model
% are transformed into travel times for every link in the network. The
% travel times are compared for the main route (from split to merge) and
% the alternative route.
%calculate the simulated travel times
[simTT] = cvn2tt(sum(cvn_up,3),sum(cvn_down,3),dt,totT,links);


figure
plot(dt*(0:1:totT),simTT(1:50,:))
xlim([0,dt*totT])
xlabel('Time [h]')
ylabel('Travel time [h]')

