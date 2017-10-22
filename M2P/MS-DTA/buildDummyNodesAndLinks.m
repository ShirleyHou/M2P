function [new_nodes,new_links,new_ODmatrices]=buildDummyNodesAndLinks(nodes,links,ODmatrices)

new_nodes=nodes;
new_links=links;
new_ODmatrices=ODmatrices;

%find all non empty od cells
sumOD=ODmatrices{1,1};
for t=2:length(ODmatrices)
    sumOD = sumOD+ODmatrices{1,t};
end
%origins
origins = find(sum(sumOD,2)>0)';
%destinations
destinations = find(sum(sumOD,1)>0);

%check if origins only have outgoing links
issued_origins=[];%initialization
map_dummyorigins=[];%initialization
linkToNode_list=links.toNode;
linkFromNode_list=links.fromNode;

for i=1:1:length(origins)
    outgoing_links=find(linkFromNode_list==origins(i));
    incoming_links=find(linkToNode_list==origins(i));
    
    if isempty(outgoing_links) && isempty(incoming_links)
        disp(['Origin ',num2str(origins(i)),' has no incoming or outgoing links!'])
    elseif (length(incoming_links)>=1)
        issued_origins=[issued_origins;origins(i)];
    end
    
end
%adding dummy origins and dummy connectors if applicable
for i=1:1:length(issued_origins)
    new_nodes=[new_nodes;{size(new_nodes,1)+1,new_nodes{issued_origins(i),2}-10^-6,new_nodes{issued_origins(i),3}+10^-6}];
    new_links=[new_links;{size(new_links,1)+1,size(new_nodes,1),issued_origins(i),0.05,60,10^6,10^6}];  %links=table(id,fromNode,toNode,length,freeSpeed,capacity,kJam);
    map_dummyorigins=[map_dummyorigins;[issued_origins(i),size(new_nodes,1)]];
end
%conversion of demand from original origin to dummy origin
for i=1:1:length(issued_origins)
    for t=1:1:length(ODmatrices)
        temp_demand=new_ODmatrices{1,t}(issued_origins(i),:);
        new_ODmatrices{1,t}(issued_origins(i),:)=zeros(1,size(new_ODmatrices{1,t},2));
        new_ODmatrices{1,t}(map_dummyorigins(i,2),:)=temp_demand;
    end
end

%check if destinations only have incoming links
issued_destinations=[];%initialization
map_dummydestinations=[];%initialization

for i=1:1:length(destinations)
    outgoing_links=find(linkFromNode_list==destinations(i));
    incoming_links=find(linkToNode_list==destinations(i));
    
    if isempty(outgoing_links) && isempty(incoming_links)
        disp(['Destination ',num2str(destinations(i)),' has no incoming or outgoing links!'])
    elseif (length(outgoing_links)>=1)
        issued_destinations=[issued_destinations;destinations(i)];
    end
    
end
%adding dummy destinations and dummy connectors if applicable
for i=1:1:length(issued_destinations)
    new_nodes=[new_nodes;{size(new_nodes,1)+1,new_nodes{issued_destinations(i),2}-10^-6,new_nodes{issued_destinations(i),3}+10^-6}];
    new_links=[new_links;{size(new_links,1)+1,issued_destinations(i),size(new_nodes,1),0.05,60,10^6,10^6}];  %links=table(id,fromNode,toNode,length,freeSpeed,capacity,kJam);
    map_dummydestinations=[map_dummydestinations;[issued_destinations(i),size(new_nodes,1)]];
end

%conversion of demand from original destination to dummy destination
for i=1:1:length(issued_destinations)
    for t=1:1:length(ODmatrices)
        temp_demand=new_ODmatrices{1,t}(:,issued_destinations(i));
        new_ODmatrices{1,t}(:,issued_destinations(i))=zeros(size(new_ODmatrices{1,t},1),1);
        new_ODmatrices{1,t}(:,map_dummydestinations(i,2))=temp_demand;
        new_ODmatrices{1,t}(map_dummydestinations(i,2),:)=zeros(1,size(new_ODmatrices{1,t},2)); % to have a square OD with new number of nodes
    end
end

end